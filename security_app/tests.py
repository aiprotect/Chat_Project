from django.test import TestCase

# Create your tests here.
# یک تست مستقل برای بررسی عملکرد GeoIP
def test_geoip():
    from security_app.advanced_monitoring import AdvancedSecurityMonitor
    monitor = AdvancedSecurityMonitor()

    test_ips = [
        '8.8.8.8',  # Google DNS (ایالات متحده)
        '5.202.128.0',  # ایران
        '127.0.0.1',  # لوکال
        'invalid_ip'  # تست خطا
    ]

    for ip in test_ips:
        print(f"\nTesting IP: {ip}")
        result = monitor._get_geoip_info(ip)
        print("Result:", result)