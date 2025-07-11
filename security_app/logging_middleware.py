# core/advanced_monitoring/middleware.py
import hashlib
import json
import platform

import django
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from django.utils.deprecation import MiddlewareMixin
from .advanced_monitoring import AdvancedSecurityMonitor

monitor = AdvancedSecurityMonitor()


class SecurityAlertSystem:
    """سیستم هشدار برای فعالیت‌های مشکوک"""

    @classmethod
    def check_anonymous_threats(cls, log_data):
        if log_data['user']['username'].startswith('anon_'):
            # هشدار برای درخواست‌های مکرر
            if cls._check_repeated_attempts(log_data):
                return 'REPEATED_ANONYMOUS_ACCESS'

            # هشدار برای دسترسی به endpointهای حساس
            if cls._check_sensitive_access(log_data):
                return 'SENSITIVE_ENDPOINT_ACCESS'

        return None

    @staticmethod
    def _check_repeated_attempts(log_data):
        from django.core.cache import cache
        cache_key = f"anon_access_{log_data['network']['ip_address']}"
        count = cache.get(cache_key, 0) + 1
        cache.set(cache_key, count, timeout=3600)
        return count > 50  # بیش از 50 درخواست در ساعت

    @staticmethod
    def _check_sensitive_access(log_data):
        sensitive_paths = [
            '/admin/', '/api/auth/', '/account/password/reset/'
        ]
        return any(
            log_data['action']['path'].startswith(path)
            for path in sensitive_paths
        )


def log_user_activity(self, request: HttpRequest, action: str, status: str = "SUCCESS"):
    """
    ثبت پیشرفته فعالیت کاربران با قابلیت‌های:
    - ردیابی کاربران احراز هویت شده و ناشناس
    - ثبت اطلاعات دستگاه و مرورگر
    - ثبت اطلاعات جغرافیایی
    - تولید شناسه منحصر به فرد برای هر رویداد
    - ثبت پارامترهای درخواست با فیلتر کردن اطلاعات حساس
    """

    try:
        # 1. جمع‌آوری اطلاعات کاربر
        user = request.user if hasattr(request, 'user') else AnonymousUser()

        # 2. تولید شناسه کاربر
        if user.is_authenticated:
            username = user.username
            user_id = str(user.id)
            session_id = request.session.session_key if hasattr(request, 'session') else None
            is_authenticated = True
        else:
            # تولید شناسه منحصر به فرد برای کاربران ناشناس
            ip = self._get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            anon_id = hashlib.sha256(
                f"{ip}{user_agent}".encode()
            ).hexdigest()[:16]
            username = f"anon_{anon_id}"
            user_id = None
            session_id = None
            is_authenticated = False

        # 3. جمع‌آوری اطلاعات دستگاه
        user_agent_obj = parse(request.META.get('HTTP_USER_AGENT', ''))
        device_info = {
            'browser': {
                'family': user_agent_obj.browser.family,
                'version': user_agent_obj.browser.version_string,
            },
            'os': {
                'family': user_agent_obj.os.family,
                'version': user_agent_obj.os.version_string,
            },
            'device': {
                'family': user_agent_obj.device.family,
                'brand': user_agent_obj.device.brand,
                'model': user_agent_obj.device.model,
            },
            'type': {
                'is_mobile': user_agent_obj.is_mobile,
                'is_tablet': user_agent_obj.is_tablet,
                'is_pc': user_agent_obj.is_pc,
                'is_bot': user_agent_obj.is_bot,
                'is_touch_capable': user_agent_obj.is_touch_capable,
            }
        }

        # 4. جمع‌آوری اطلاعات شبکه
        ip_address = self._get_client_ip(request)
        network_info = {
            'ip': ip_address,
            'user_agent': str(user_agent_obj),
            'referrer': request.META.get('HTTP_REFERER'),
            'host': request.get_host(),
            'scheme': request.scheme,
        }

        # 5. جمع‌آوری اطلاعات درخواست
        action_info = {
            'type': action,
            'path': request.path,
            'method': request.method,
            'status': status,
            'full_url': request.build_absolute_uri(),
            'parameters': self._sanitize_params(request),
            'headers': self._filter_headers(request),
        }

        # 6. دریافت اطلاعات جغرافیایی
        location_info = self._get_geoip_info(ip_address)

        # 7. تحلیل امنیتی
        security_analysis = self._analyze_for_threats(request, action)

        # 8. ایجاد شناسه منحصر به فرد رویداد
        event_id = hashlib.sha256(
            f"{datetime.now().timestamp()}{ip_address}{username}{action}{status}".encode()
        ).hexdigest()

        # 9. ساخت ساختار کامل لاگ
        log_data = {
            'event_id': event_id,
            'timestamp': datetime.now().isoformat(),
            'user': {
                'username': username,
                'authenticated': is_authenticated,
                'user_id': user_id,
                'session_id': session_id,
            },
            'device': device_info,
            'network': network_info,
            'action': action_info,
            'location': location_info,
            'security_analysis': security_analysis,
            'system': {
                'django_version': django.get_version(),
                'python_version': platform.python_version(),
            }
        }

        # 10. ثبت لاگ
        self.logger.info(json.dumps(log_data, ensure_ascii=False))

        # 11. بررسی فعالیت‌های مشکوک
        self._check_for_suspicious_activity(log_data)

        return log_data

    except Exception as e:
        self.logger.error(f"Failed to log user activity: {str(e)}", exc_info=True)
        return None


def _sanitize_params(self, request):
    """پاکسازی پارامترهای حساس قبل از ثبت"""
    sensitive_keys = ['password', 'secret', 'token', 'key', 'credit', 'cvv']
    params = {}

    if request.method == 'GET':
        source = request.GET
    elif request.method == 'POST':
        source = request.POST
    else:
        return {}

    for key, value in source.items():
        if any(sensitive in key.lower() for sensitive in sensitive_keys):
            params[key] = '*****REDACTED*****'
        else:
            params[key] = str(value)[:100]  # محدودیت طول برای جلوگیری از لاگ‌های بسیار بزرگ

    return params


def _filter_headers(self, request):
    """فیلتر کردن هدرهای حساس"""
    sensitive_headers = ['Authorization', 'Cookie', 'X-CSRFToken']
    headers = {}

    for header, value in request.META.items():
        if any(h in header for h in ['HTTP_', 'CONTENT_']):
            clean_header = header.replace('HTTP_', '').replace('_', '-').title()
            if clean_header not in sensitive_headers:
                headers[clean_header] = str(value)[:200]  # محدودیت طول

    return headers

class AdvancedMonitoringMiddleware(MiddlewareMixin):
    """میدلور مانیتورینگ پیشرفته برای ردیابی تمام درخواست‌ها"""

    def process_request(self, request):
        # ردیابی درخواست‌های ورودی
        if request.path.startswith('/admin/'):
            monitor.log_user_activity(request, 'admin_access')
        elif request.path.startswith('/login/'):
            monitor.log_user_activity(request, 'login_attempt')
        else:
            monitor.log_user_activity(request, 'page_view')

    def process_response(self, request, response):
        # ردیابی پاسخ‌های خروجی
        if response.status_code >= 400:
            monitor.log_user_activity(
                request,
                f'error_{response.status_code}',
                status='FAILED'
            )
        return response

    def process_exception(self, request, exception):
        # ردیابی خطاهای سیستمی
        monitor.log_user_activity(
            request,
            f'system_exception_{type(exception).__name__}',
            status='CRITICAL'
        )