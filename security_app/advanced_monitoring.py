# core/advanced_monitoring/security_system.py
import logging
import re
import hashlib
from datetime import datetime

# core/advanced_monitoring/security_system.py

from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from user_agents import parse
import os
from django.conf import settings

class AdvancedSecurityMonitor:
    """
    سیستم مانیتورینگ امنیتی پیشرفته با قابلیت‌های:
    - ردیابی کامل فعالیت کاربران
    - تشخیص رفتارهای مشکوک
    - ثبت تمامی رویدادهای امنیتی
    - تحلیل بلادرنگ
    """

    def __init__(self):
        self.logger = logging.getLogger('django.security')
        self.suspicious_activities = []

    def log_user_activity(self, request: HttpRequest, action: str, status: str = "SUCCESS"):
        """ثبت کامل فعالیت کاربر"""

        # استخراج اطلاعات کاربر
        user = request.user if hasattr(request, 'user') else AnonymousUser()
        username = user.username if user.is_authenticated else 'anonymous'

        # جمع‌آوری اطلاعات دستگاه
        user_agent = parse(request.META.get('HTTP_USER_AGENT', ''))
        device_info = {
            'browser': user_agent.browser.family,
            'os': user_agent.os.family,
            'device': user_agent.device.family,
            'is_mobile': user_agent.is_mobile,
            'is_tablet': user_agent.is_tablet,
            'is_pc': user_agent.is_pc,
            'is_bot': user_agent.is_bot
        }

        # جمع‌آوری اطلاعات شبکه
        ip = self._get_client_ip(request)
        session_key = request.session.session_key if hasattr(request, 'session') else None

        # ایجاد شناسه منحصر به فرد برای هر رویداد
        event_id = hashlib.sha256(
            f"{datetime.now().timestamp()}{ip}{username}{action}".encode()
        ).hexdigest()

        # ثبت لاگ کامل
        log_data = {
            'event_id': event_id,
            'timestamp': datetime.now().isoformat(),
            'user': {
                'username': username,
                'authenticated': user.is_authenticated,
                'user_id': user.id if user.is_authenticated else None,
                'session_id': session_key,
            },
            'device': device_info,
            'network': {
                'ip_address': ip,
                'user_agent': str(user_agent),
                'referrer': request.META.get('HTTP_REFERER'),
            },
            'action': {
                'type': action,
                'path': request.path,
                'method': request.method,
                'status': status,
                'parameters': self._sanitize_params(request),
            },
            'location': self._get_geoip_info(ip),
            'security_analysis': self._analyze_for_threats(request, action)
        }

        self.logger.info(log_data)
        self._check_for_suspicious_activity(log_data)

    def _get_client_ip(self, request):
        """استخراج IP واقعی کاربر با توجه به پروکسی‌ها"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def _sanitize_params(self, request):
        """پاکسازی پارامترهای حساس قبل از ثبت"""
        sensitive_keys = ['password', 'secret', 'token', 'key']
        params = {}

        if request.method == 'GET':
            params = dict(request.GET)
        elif request.method == 'POST':
            params = dict(request.POST)

        for key in params:
            if any(sensitive in key.lower() for sensitive in sensitive_keys):
                params[key] = '*****REDACTED*****'

        return params



    def _get_geoip_info(self, ip):
        """دریافت اطلاعات جغرافیایی با مدیریت خطاهای بهبود یافته"""
        if ip in ['127.0.0.1', '::1']:
            return {
                'type': 'local',
                'warning': 'Localhost access'
            }

        try:
            from geoip2 import database

            # ساخت مسیر کامل فایل
            geoip_db_path = os.path.join(settings.GEOIP_PATH, settings.GEOIP_CITY)

            # بررسی وجود فایل
            if not os.path.exists(geoip_db_path):
                raise FileNotFoundError(f"GeoIP database not found at {geoip_db_path}")

            # خواندن اطلاعات جغرافیایی
            with database.Reader(geoip_db_path) as reader:
                try:
                    response = reader.city(ip)
                    return {
                        'type': 'remote',
                        'country': response.country.name,
                        'country_code': response.country.iso_code,
                        'city': response.city.name if response.city.name else 'Unknown',
                        'latitude': float(response.location.latitude),
                        'longitude': float(response.location.longitude),
                        'accuracy_radius': response.location.accuracy_radius
                    }
                except database.AddressNotFoundError:
                    return {
                        'type': 'unknown',
                        'message': 'IP address not found in database'
                    }

        except Exception as e:
            return {
                'type': 'error',
                'error': str(e),
                'ip': ip,
                'debug': {
                    'geoip_path': settings.GEOIP_PATH,
                    'geoip_city': settings.GEOIP_CITY,
                    'actual_path': os.path.join(settings.GEOIP_PATH, settings.GEOIP_CITY)
                    if hasattr(settings, 'GEOIP_PATH') else 'Not configured'
                }
            }

    def _analyze_for_threats(self, request, action):
        """تحلیل امنیتی فعالیت"""
        threats = []

        # تشخیص تلاش برای دسترسی غیرمجاز
        if action == 'login_attempt' and not request.user.is_authenticated:
            threats.append('POTENTIAL_BRUTE_FORCE')

        # تشخیص تغییرات غیرعادی در حساب کاربری
        if action == 'profile_update' and 'email' in request.POST:
            threats.append('ACCOUNT_TAKEOVER_ATTEMPT')

        # تشخیص فعالیت از مکان‌های غیرعادی
        geo_info = self._get_geoip_info(self._get_client_ip(request))
        if geo_info and hasattr(request.user, 'last_known_location'):
            if geo_info['country'] != request.user.last_known_location:
                threats.append('UNUSUAL_LOCATION_ACCESS')

        return threats if threats else 'CLEAN'

    def _check_for_suspicious_activity(self, log_data):
        """بررسی فعالیت‌های مشکوک"""
        if log_data['security_analysis'] != 'CLEAN':
            self.suspicious_activities.append(log_data)
            self._trigger_alert(log_data)

    def _trigger_alert(self, log_data):
        """ارسال هشدار امنیتی"""
        # ارسال ایمیل به مدیر سیستم
        from django.core.mail import mail_admins
        mail_admins(
            subject=f"هشدار امنیتی: فعالیت مشکوک شناسایی شد - {log_data['event_id']}",
            message=str(log_data)
        )

        # ذخیره در سیستم هشدارهای امنیتی
        from .models import SecurityAlert
        SecurityAlert.objects.create(
            event_id=log_data['event_id'],
            alert_type=log_data['security_analysis'],
            details=log_data
        )