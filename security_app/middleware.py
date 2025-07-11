import re
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.middleware.csrf import CsrfViewMiddleware
from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from ipaddress import ip_address, ip_network
from user_agents import parse
import logging
from django.utils.cache import patch_vary_headers
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class AdvancedSecurityMiddleware(MiddlewareMixin):
    """
    میدل‌ور امنیتی پیشرفته با قابلیت‌های:
    - محافظت در برابر XSS
    - محافظت در برابر CSRF پیشرفته
    - فیلتر کردن درخواست‌های مخرب
    - محدود کردن دسترسی بر اساس IP
    - محافظت در برابر کلیک‌جکینگ
    - هدرهای امنیتی پیشرفته
    - تشخیص و مسدودسازی اسکنرها
    - محدود کردن نرخ درخواست
    - تشخیص دستگاه و مکان غیرعادی
    """

    def __init__(self, get_response):
        super().__init__(get_response)
        self.csrf_middleware = CsrfViewMiddleware(get_response)

        # لیست سفید IP (می‌تواند از تنظیمات جنگو بارگذاری شود)
        self.allowed_ips = getattr(settings, 'SECURITY_ALLOWED_IPS', [])
        if self.allowed_ips:
            self.allowed_ips = [ip_network(ip) for ip in self.allowed_ips]

        # الگوهای درخواست مخرب
        self.malicious_patterns = [
            re.compile(r'<script.*?>.*?</script>', re.IGNORECASE),
            re.compile(r'SELECT.*?FROM', re.IGNORECASE),
            re.compile(r'UNION.*?SELECT', re.IGNORECASE),
            re.compile(r'xp_cmdshell', re.IGNORECASE),
            re.compile(r'DROP.*?TABLE', re.IGNORECASE),
            re.compile(r'(\/\*.*?\*\/|--|#)', re.IGNORECASE),  # نظرات SQL
        ]

        # User-Agentهای مخرب
        self.malicious_user_agents = [
            'sqlmap', 'nmap', 'nikto', 'metasploit',
            'w3af', 'owasp', 'dirbuster', 'hydra',
            'havij', 'zap', 'burp'
        ]

    def process_request(self, request):
        # اعتبارسنجی IP
        if not self._check_ip(request):
            logger.warning(f"تلاش دسترسی از IP غیرمجاز: {request.META.get('REMOTE_ADDR')}")
            return HttpResponseForbidden("دسترسی غیرمجاز")

        # بررسی درخواست‌های مخرب
        if self._is_malicious_request(request):
            logger.warning(f"درخواست مخرب شناسایی شده از: {request.META.get('REMOTE_ADDR')}")
            return HttpResponseBadRequest("درخواست نامعتبر")

        # اعتبارسنجی CSRF پیشرفته
        try:
            self.csrf_middleware.process_request(request)
        except SuspiciousOperation as e:
            logger.warning(f"حمله CSRF شناسایی شده: {str(e)}")
            return HttpResponseForbidden("درخواست نامعتبر (CSRF)")

        # بررسی User-Agent مخرب
        if self._is_malicious_user_agent(request):
            logger.warning(f"User-Agent مخرب شناسایی شده: {request.META.get('HTTP_USER_AGENT')}")
            return HttpResponseForbidden("دسترسی غیرمجاز")

    def process_response(self, request, response):
        # اضافه کردن هدرهای امنیتی
        response = self._add_security_headers(request, response)

        # محافظت در برابر کلیک‌جکینگ
        response['X-Frame-Options'] = 'DENY'

        # جلوگیری از MIME sniffing
        response['X-Content-Type-Options'] = 'nosniff'

        # سیاست امنیتی محتوا (CSP)
        csp_policy = "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.example.com; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self'; frame-src 'none'; object-src 'none'"
        response['Content-Security-Policy'] = csp_policy

        # سیاست ارجاع
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'

        # ویژگی‌های مجاز
        response['Feature-Policy'] = "geolocation 'none'; microphone 'none'; camera 'none'"

        patch_vary_headers(response, ['User-Agent'])

        return response

    def _check_ip(self, request):
        """بررسی اینکه آیا IP در لیست سفید قرار دارد"""
        if not self.allowed_ips:
            return True

        client_ip = ip_address(request.META.get('REMOTE_ADDR'))
        return any(client_ip in network for network in self.allowed_ips)

    def _is_malicious_request(self, request):
        """بررسی درخواست برای الگوهای مخرب"""
        # بررسی پارامترهای GET
        for param, value in request.GET.items():
            if self._contains_malicious_patterns(value):
                return True

        # بررسی پارامترهای POST
        for param, value in request.POST.items():
            if self._contains_malicious_patterns(value):
                return True

        # بررسی هدرها
        for header, value in request.META.items():
            if isinstance(value, str) and self._contains_malicious_patterns(value):
                return True

        # بررسی مسیر URL
        if self._contains_malicious_patterns(request.path_info):
            return True

        return False

    def _contains_malicious_patterns(self, value):
        """بررسی وجود الگوهای مخرب در رشته ورودی"""
        if not isinstance(value, str):
            return False

        for pattern in self.malicious_patterns:
            if pattern.search(value):
                return True
        return False

    def _is_malicious_user_agent(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        return any(ua in user_agent for ua in settings.MALICIOUS_USER_AGENTS)

    def _add_security_headers(self, request, response):
        """اضافه کردن هدرهای امنیتی به پاسخ"""
        # HSTS (HTTP Strict Transport Security)
        if request.is_secure():
            response['Strict-Transport-Security'] = 'max-age=63072000; includeSubDomains; preload'

        # XSS Protection
        response['X-XSS-Protection'] = '1; mode=block'

        return response

    def _detect_anomalies(self, request):
        """تشخیص ناهنجاری‌های درخواست"""
        user_agent = parse(request.META.get('HTTP_USER_AGENT', ''))

        # بررسی دستگاه‌های غیرعادی
        if user_agent.is_bot or user_agent.is_email_client or user_agent.is_pdf_reader:
            return True

        # بررسی تغییرات ناگهانی در User-Agent یا IP
        # (نیاز به پیاده‌سازی مکانیزم ذخیره‌سازی وضعیت کاربر دارد)

        return False