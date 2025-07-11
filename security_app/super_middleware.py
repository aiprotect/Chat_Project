import re
import socket
import logging
from django.http import HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseServerError
from django.conf import settings
from django.core.exceptions import SuspiciousOperation, DisallowedHost
from ipaddress import ip_address, ip_network
from user_agents import parse
from hashlib import sha256
from time import time
from functools import wraps
import hmac
import pytz
from datetime import datetime, timedelta
import tldextract
import dns.resolver

logger = logging.getLogger('security')

class AdvancedSecurityMiddleware:
    """
    میدلور امنیتی پیشرفته با لایه‌های متعدد حفاظتی
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.security_headers = {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Referrer-Policy': 'strict-origin-when-cross-origin',
            'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.example.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; img-src 'self' data: https://*.example.com; font-src 'self' https://fonts.gstatic.com; connect-src 'self' https://api.example.com; frame-ancestors 'none';",
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains; preload',
            'Permissions-Policy': 'geolocation=(), microphone=(), camera=(), payment=()',
            'Cross-Origin-Embedder-Policy': 'require-corp',
            'Cross-Origin-Opener-Policy': 'same-origin',
            'Cross-Origin-Resource-Policy': 'same-origin',
        }
        
        # لیست سیاه IPها و User-Agentها
        self.blacklisted_ips = self._load_blacklist('ip_blacklist.txt')
        self.blacklisted_user_agents = self._load_blacklist('ua_blacklist.txt')
        
        # لیست ابزارهای اسکن مانند nmap
        self.scanner_tools = [
            'nmap', 'nikto', 'metasploit', 'sqlmap', 'wpscan', 
            'burpsuite', 'owasp zap', 'acunetix', 'nessus',
            'dirbuster', 'gobuster', 'hydra', 'john the ripper'
        ]
        
        # تنظیمات محدودیت نرخ
        self.rate_limit = 100  # درخواست در دقیقه
        self.rate_limit_window = 60  # ثانیه
        self.request_tracker = {}
        
        # تنظیمات فیلتر کردن حملات
        # در super_middleware.py
        self.sql_injection_patterns = [
            r'(\%27)|(\')|(\-\-)',
            r'((\%3D)|(=))[^\n]*((\%27)|(\')|(\-\-))',
            r'\w*((\%27)|(\'))((\%6F)|o|(\%4F))((\%72)|r|(\%52))',
            r'((\%27)|(\'))union',
            r'exec(\s|\+)+(s|x)p\w+',
        ]

        self.xss_patterns = [
            r'<script[^>]*>.*?</script>',
            r'on\w+\s*=\s*"[^"]*"',
            r'on\w+\s*=\s*\'[^\']*\'',
            r'on\w+\s*=\s*[^\s>]+',
            r'javascript:\s*\w+\([^)]*\)',
        ]
        
        self.path_traversal_patterns = [
            r'\.\./',
            r'\.\.\\',
            r'%2e%2e/',
            r'%252e%252e/',
        ]
        
        # تنظیمات احراز هویت پیشرفته
        self.auth_fail_limit = 5
        self.auth_fail_window = 300  # 5 دقیقه
        self.auth_fail_tracker = {}
        
        # تنظیمات فیلتر کردن هدرها
        self.suspicious_headers = [
            'x-forwarded-host',
            'x-forwarded-for',
            'x-forwarded-proto',
            'x-originating-ip',
            'x-remote-ip',
            'x-remote-addr',
        ]

    def _load_blacklist(self, filename):
        """بارگذاری لیست سیاه از فایل"""
        try:
            with open(filename, 'r') as f:
                return set(line.strip() for line in f if line.strip())
        except FileNotFoundError:
            return set()

    def _is_scanner_tool(self, user_agent):
        """تشخیص ابزارهای اسکن مانند nmap"""
        if not user_agent:
            return False
            
        user_agent_lower = user_agent.lower()
        return any(tool in user_agent_lower for tool in self.scanner_tools)

    def _check_sql_injection(self, value):
        """تشخیص حملات SQL injection"""
        if not value:
            return False
            
        if isinstance(value, str):
            for pattern in self.sql_injection_patterns:
                if re.search(pattern, value, re.IGNORECASE):
                    return True
        return False

    def _check_xss(self, value):
        """تشخیص حملات XSS"""
        if not value:
            return False
            
        if isinstance(value, str):
            for pattern in self.xss_patterns:
                if re.search(pattern, value, re.IGNORECASE):
                    return True
        return False

    def _check_path_traversal(self, value):
        """تشخیص حملات Path Traversal"""
        if not value:
            return False
            
        if isinstance(value, str):
            for pattern in self.path_traversal_patterns:
                if re.search(pattern, value, re.IGNORECASE):
                    return True
        return False

    def _check_rate_limit(self, ip):
        """اعمال محدودیت نرخ درخواست"""
        now = time()
        window_start = now - self.rate_limit_window
        
        # حذف درخواست‌های قدیمی
        self.request_tracker[ip] = [
            timestamp for timestamp in self.request_tracker.get(ip, []) 
            if timestamp >= window_start
        ]
        
        # اضافه کردن درخواست جدید
        self.request_tracker[ip].append(now)
        
        # بررسی تعداد درخواست‌ها
        if len(self.request_tracker[ip]) > self.rate_limit:
            logger.warning(f'Rate limit exceeded for IP: {ip}')
            return False
            
        return True

    def _check_auth_failures(self, ip):
        """پیگیری شکست‌های احراز هویت"""
        now = time()
        window_start = now - self.auth_fail_window
        
        # حذف شکست‌های قدیمی
        self.auth_fail_tracker[ip] = [
            timestamp for timestamp in self.auth_fail_tracker.get(ip, []) 
            if timestamp >= window_start
        ]
        
        # بررسی تعداد شکست‌ها
        if len(self.auth_fail_tracker[ip]) >= self.auth_fail_limit:
            logger.warning(f'Too many auth failures for IP: {ip}')
            return False
            
        return True

    def _log_auth_failure(self, ip):
        """ثبت شکست احراز هویت"""
        if ip not in self.auth_fail_tracker:
            self.auth_fail_tracker[ip] = []
        self.auth_fail_tracker[ip].append(time())

    def _validate_host_header(self, request):
        if settings.DEBUG:
            return  # هیچ بررسی در محیط توسعه انجام نده

        host = request.get_host()
        allowed_hosts = getattr(settings, 'ALLOWED_HOSTS', [])

        if not any(
                host == allowed or
                host.startswith(f'{allowed}:') or  # برای پورت‌ها
                host.endswith(f'.{allowed}')
                for allowed in allowed_hosts
        ):
            raise DisallowedHost(f"Invalid HTTP_HOST header: {host}")

        # بررسی سایر میزبان‌ها
        allowed_hosts = getattr(settings, 'ALLOWED_HOSTS', [])
        if not any(
                host == allowed or
                host.endswith(f'.{allowed}') or
                host_without_port == allowed.split(':')[0]
                for allowed in allowed_hosts
        ):
            raise DisallowedHost(f"Invalid HTTP_HOST header: {host}")

    def _check_suspicious_headers(self, request):
        """بررسی هدرهای مشکوک"""
        for header in self.suspicious_headers:
            if header in request.META:
                logger.warning(f'Suspicious header detected: {header}')
                return False
        return True

    def _check_http_method(self, request):
        """بررسی متد HTTP"""
        allowed_methods = ['GET', 'POST', 'HEAD', 'OPTIONS']
        if request.method not in allowed_methods:
            logger.warning(f'Disallowed HTTP method: {request.method}')
            return False
        return True

    def _check_request_params(self, request):
        """بررسی پارامترهای درخواست برای حملات احتمالی"""
        # بررسی GET پارامترها
        for param, value in request.GET.items():
            if (self._check_sql_injection(value) or 
                self._check_xss(value) or 
                self._check_path_traversal(value)):
                logger.warning(f'Malicious parameter detected - Param: {param}, Value: {value}')
                return False
                
        # بررسی POST پارامترها
        for param, value in request.POST.items():
            if (self._check_sql_injection(value) or 
                self._check_xss(value) or 
                self._check_path_traversal(value)):
                logger.warning(f'Malicious parameter detected - Param: {param}, Value: {value}')
                return False
                
        # بررسی کوکی‌ها
        for cookie_name, cookie_value in request.COOKIES.items():
            if (self._check_sql_injection(cookie_value) or 
                self._check_xss(cookie_value) or 
                self._check_path_traversal(cookie_value)):
                logger.warning(f'Malicious cookie detected - Cookie: {cookie_name}, Value: {cookie_value}')
                return False
                
        return True

    def _check_user_agent(self, request):
        """بررسی User-Agent"""
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        # بررسی ابزارهای اسکن
        if self._is_scanner_tool(user_agent):
            logger.warning(f'Scanner tool detected: {user_agent}')
            return False
            
        # بررسی User-Agentهای لیست سیاه
        if user_agent in self.blacklisted_user_agents:
            logger.warning(f'Blacklisted user agent: {user_agent}')
            return False
            
        return True

    def _check_ip_address(self, request):
        ip = request.META.get('REMOTE_ADDR')

        # اجازه دسترسی به IPهای لوکال در محیط توسعه
        if settings.DEBUG and ip in ['127.0.0.1', '::1']:
            return True

        # بررسی IPهای لیست سیاه
        if ip in self.blacklisted_ips:
            logger.warning(f'Blacklisted IP: {ip}')
            return False

        # بررسی IPهای خصوصی
        try:
            ip_obj = ip_address(ip)
            if ip_obj.is_private and not settings.DEBUG:  # فقط در محیط تولید بررسی شود
                logger.warning(f'Private IP access attempt: {ip}')
                return False
        except ValueError:
            pass

        return True

    def _add_security_headers(self, response):
        """اضافه کردن هدرهای امنیتی"""
        for header, value in self.security_headers.items():
            response[header] = value
        return response

    def _log_security_event(self, request, event_type, details):
        """ثبت رویداد امنیتی"""
        ip = request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        method = request.method
        path = request.get_full_path()
        
        log_entry = (
            f"Security Event: {event_type}\n"
            f"IP: {ip}\n"
            f"User-Agent: {user_agent}\n"
            f"Method: {method}\n"
            f"Path: {path}\n"
            f"Details: {details}\n"
            f"Timestamp: {datetime.now(pytz.utc).isoformat()}\n"
        )
        
        logger.warning(log_entry)

    def process_request(self, request):
        """پردازش درخواست ورودی"""
        
        # اعتبارسنجی هدر Host
        try:
            self._validate_host_header(request)
        except DisallowedHost:
            self._log_security_event(request, 'INVALID_HOST_HEADER', 'Invalid or disallowed host header')
            return HttpResponseForbidden('Invalid host header')

        # بررسی IP آدرس
        if not self._check_ip_address(request):
            self._log_security_event(request, 'BLACKLISTED_IP', 'Access attempt from blacklisted IP')
            return HttpResponseForbidden('Access denied')

        # بررسی User-Agent
        if not self._check_user_agent(request):
            self._log_security_event(request, 'MALICIOUS_USER_AGENT', 'Scanner tool or blacklisted user agent detected')
            return HttpResponseForbidden('Access denied')

        # بررسی متد HTTP
        if not self._check_http_method(request):
            self._log_security_event(request, 'INVALID_HTTP_METHOD', 'Disallowed HTTP method used')
            return HttpResponseNotAllowed(['GET', 'POST', 'HEAD'])

        # بررسی هدرهای مشکوک
        if not self._check_suspicious_headers(request):
            self._log_security_event(request, 'SUSPICIOUS_HEADER', 'Suspicious header detected')
            return HttpResponseForbidden('Invalid request headers')

        # بررسی پارامترهای درخواست
        if not self._check_request_params(request):
            self._log_security_event(request, 'MALICIOUS_PARAMETERS', 'Malicious parameters detected in request')
            return HttpResponseForbidden('Invalid request parameters')

        # بررسی محدودیت نرخ
        ip = request.META.get('REMOTE_ADDR')
        if not self._check_rate_limit(ip):
            self._log_security_event(request, 'RATE_LIMIT_EXCEEDED', 'Too many requests in short time')
            return HttpResponseForbidden('Rate limit exceeded. Please try again later.')

        return None

    def process_response(self, request, response):
        """پردازش پاسخ خروجی"""
        
        # اضافه کردن هدرهای امنیتی
        response = self._add_security_headers(response)
        
        # حذف هدرهای حساس
        sensitive_headers = ['Server', 'X-Powered-By', 'X-AspNet-Version']
        for header in sensitive_headers:
            if header in response:
                del response[header]
        
        return response

    def process_exception(self, request, exception):
        """پردازش استثناها"""
        if isinstance(exception, SuspiciousOperation):
            self._log_security_event(request, 'SUSPICIOUS_OPERATION', str(exception))
            return HttpResponseForbidden('Invalid request')
            
        return None

    def __call__(self, request):
        # پردازش درخواست
        response = self.process_request(request)
        if response:
            return response
            
        # دریافت پاسخ از لایه‌های بعدی
        response = self.get_response(request)
        
        # پردازش پاسخ
        response = self.process_response(request, response)
        
        return response


class AdvancedAuthMiddleware:
    """
    میدلور احراز هویت پیشرفته با مکانیزم‌های امنیتی اضافه
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.security_headers = {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
        }
        
    def _check_session_security(self, request):
        """بررسی امنیت نشست"""
        if not request.user.is_authenticated:
            return True
            
        # بررسی تغییر User-Agent
        current_ua = request.META.get('HTTP_USER_AGENT', '')
        session_ua = request.session.get('user_agent')
        
        if session_ua and session_ua != current_ua:
            logger.warning(f'Session hijacking attempt detected for user {request.user.username}')
            return False
            
        # بررسی تغییر IP
        current_ip = request.META.get('REMOTE_ADDR')
        session_ip = request.session.get('ip_address')
        
        if session_ip and session_ip != current_ip:
            logger.warning(f'Session hijacking attempt detected for user {request.user.username}')
            return False
            
        return True

    def _enforce_2fa(self, request):
        """اجبار به احراز هویت دو مرحله‌ای"""
        if not request.user.is_authenticated:
            return True
            
        if request.path in ['/2fa/verify', '/logout', '/static/']:
            return True
            
        if not request.session.get('2fa_verified'):
            logger.warning(f'2FA required for user {request.user.username}')
            return False
            
        return True

    def _check_password_strength(self, request):
        """بررسی قدرت رمز عبور"""
        if request.method != 'POST' or 'password' not in request.POST:
            return True
            
        password = request.POST['password']
        
        # حداقل طول
        if len(password) < 12:
            return False
            
        # ترکیب کاراکترها
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)
        
        if not (has_upper and has_lower and has_digit and has_special):
            return False
            
        return True

    def process_request(self, request):
        """پردازش درخواست"""
        
        # بررسی امنیت نشست
        if not self._check_session_security(request):
            return HttpResponseForbidden('Session security violation detected')
            
        # اعمال 2FA
        # if not self._enforce_2fa(request):
        #     return HttpResponseForbidden('Two-factor authentication required')
            
        # بررسی قدرت رمز عبور
        # if not self._check_password_strength(request):
        #     return HttpResponseForbidden('Password does not meet security requirements')
            
        return None

    def process_response(self, request, response):
        """پردازش پاسخ"""
        
        # اضافه کردن هدرهای امنیتی
        for header, value in self.security_headers.items():
            response[header] = value
            
        # تنظیم نشست امن
        if request.user.is_authenticated:
            if not request.session.get('user_agent'):
                request.session['user_agent'] = request.META.get('HTTP_USER_AGENT', '')
                
            if not request.session.get('ip_address'):
                request.session['ip_address'] = request.META.get('REMOTE_ADDR')
                
            # تنظیم کوکی امن
            if settings.SESSION_COOKIE_SECURE:
                response.set_cookie(
                    settings.SESSION_COOKIE_NAME,
                    request.session.session_key,
                    secure=True,
                    httponly=True,
                    samesite='Strict',
                    max_age=settings.SESSION_COOKIE_AGE,
                    domain=settings.SESSION_COOKIE_DOMAIN,
                )
                
        return response

    def __call__(self, request):
        response = self.process_request(request)
        if response:
            return response
            
        response = self.get_response(request)
        response = self.process_response(request, response)
        
        return response


class RequestLoggingMiddleware:
    """
    میدلور ثبت درخواست‌ها برای تحلیل امنیتی
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def _should_log_request(self, request):
        """تعیین آیا درخواست باید ثبت شود"""
        # عدم ثبت درخواست‌های استاتیک
        if request.path.startswith('/static/') or request.path.startswith('/media/'):
            return False
            
        # عدم ثبت درخواست‌های سلامت
        if request.path == '/health/' or request.path == '/ping/':
            return False
            
        return True

    def process_request(self, request):
        """پردازش درخواست"""
        if self._should_log_request(request):
            ip = request.META.get('REMOTE_ADDR')
            method = request.method
            path = request.get_full_path()
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            
            log_entry = (
                f"Request: {method} {path}\n"
                f"IP: {ip}\n"
                f"User-Agent: {user_agent}\n"
                f"Timestamp: {datetime.now(pytz.utc).isoformat()}\n"
            )
            
            logger.info(log_entry)
            
        return None

    def __call__(self, request):
        response = self.process_request(request)
        if response:
            return response
            
        response = self.get_response(request)
        return response
