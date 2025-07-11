# core/monitoring/performance.py
import psutil
from prometheus_client import Gauge, start_http_server


class PerformanceMonitor:
    def __init__(self):
        self.cpu_usage = Gauge('django_cpu_usage', 'CPU usage percentage')
        self.memory_usage = Gauge('django_memory_usage', 'Memory usage percentage')
        self.request_count = Gauge('django_requests', 'HTTP requests count')

    def start_monitoring(self):
        start_http_server(8001)
        while True:
            self.update_metrics()
            time.sleep(5)

    def update_metrics(self):
        self.cpu_usage.set(psutil.cpu_percent())
        self.memory_usage.set(psutil.virtual_memory().percent)