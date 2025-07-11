# core/security/ids.py
from datetime import datetime, timedelta
from django.core.cache import cache


class AdvancedIntrusionDetection:
    @classmethod
    def detect_brute_force(cls, request):
        ip = cls.get_client_ip(request)
        cache_key = f"login_attempts_{ip}"
        attempts = cache.get(cache_key, 0) + 1
        cache.set(cache_key, attempts, timeout=300)

        if attempts > 10:
            self.log_security_event(
                event_type="BRUTE_FORCE_ATTEMPT",
                severity="CRITICAL",
                request=request,
                details=f"Multiple failed login attempts from {ip}"
            )
            return True
        return False

    @classmethod
    def detect_sqli(cls, request):
        sql_keywords = ["'", "--", ";", "union", "select", "drop", "insert"]
        for param in request.GET.values():
            if any(keyword in param.lower() for keyword in sql_keywords):
                self.log_security_event(
                    event_type="SQLI_ATTEMPT",
                    severity="HIGH",
                    request=request,
                    details=f"Possible SQL injection attempt in {request.path}"
                )
                return True
        return False