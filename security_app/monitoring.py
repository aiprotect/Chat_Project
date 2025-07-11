# core/monitoring.py
import logging
from django.utils import timezone


# core/monitoring.py
class SecureFormatter(logging.Formatter):
    def format(self, record):
        # تنظیم مقادیر پیش‌فرض
        record.ip = getattr(record, 'ip', '0.0.0.0')
        record.user = getattr(record, 'user', 'anonymous')

        # حذف کدهای رنگ از پیام (ANSI escape codes)
        message = super().format(record)
        clean_message = re.sub(r'\x1b\[[0-9;]*m', '', message)
        return clean_message