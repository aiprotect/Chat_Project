
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class UserActivityLog(models.Model):
    """ذخیره تمام فعالیت‌های کاربران"""
    event_id = models.CharField(max_length=64, unique=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField()
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    action_type = models.CharField(max_length=100)
    request_path = models.CharField(max_length=255)
    request_method = models.CharField(max_length=10)
    status = models.CharField(max_length=20)
    device_info = models.JSONField()
    location_info = models.JSONField(null=True)
    parameters = models.JSONField()

    class Meta:
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['ip_address', 'timestamp']),
        ]


class SecurityAlert(models.Model):
    """ذخیره هشدارهای امنیتی"""
    ALERT_TYPES = (
        ('BRUTE_FORCE', 'تلاش برای حمله Brute Force'),
        ('UNUSUAL_LOCATION', 'دسترسی از مکان غیرعادی'),
        ('ACCOUNT_TAKEOVER', 'تلاش برای تصاحب حساب'),
        ('SUSPICIOUS_ACTIVITY', 'فعالیت مشکوک'),
    )

    event_id = models.CharField(max_length=64)
    alert_type = models.CharField(max_length=50, choices=ALERT_TYPES)
    detected_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)
    details = models.JSONField()
    related_activity = models.ForeignKey(
        UserActivityLog,
        null=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"{self.get_alert_type_display()} - {self.event_id}"