# core/security/threat_intelligence.py
import requests
from django.conf import settings


class ThreatIntelligenceFeed:
    def __init__(self):
        self.feeds = [
            "https://feeds.example.com/threats",
            "https://threatintel.example.org/feed"
        ]
        self.cache_timeout = 3600  # 1 hour

    def check_ip_reputation(self, ip):
        cache_key = f"threat_ip_{ip}"
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result

        for feed in self.feeds:
            response = requests.get(
                f"{feed}/check?ip={ip}",
                headers={"Authorization": f"Bearer {settings.THREAT_FEED_API_KEY}"}
            )
            if response.status_code == 200:
                result = response.json()
                if result.get('malicious'):
                    cache.set(cache_key, True, self.cache_timeout)
                    return True

        cache.set(cache_key, False, self.cache_timeout)
        return False