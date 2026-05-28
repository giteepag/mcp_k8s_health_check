from app.services.prometheus_client import PrometheusClient
from app.utils.health_score import normalize

CPU_QUERY = """
100 - (avg(rate(container_cpu_usage_seconds_total[5m])) * 100)
"""


class CPUHealthTool:
    def __init__(self):
        self.prom = PrometheusClient()

    def get_cpu_usage(self):
        return self.prom.query_scalar(CPU_QUERY)

    def evaluate(self):
        raw = self.get_cpu_usage()

        cpu_usage = float(raw)

        score = normalize(
            value=cpu_usage,
            warning=60,
            critical=90
        )

        return {
            "metric": "cpu",
            "usage_percent": cpu_usage,
            "score": score,
            "status": self._status(score)
        }

    def _status(self, score):
        if score > 80:
            return "healthy"
        elif score > 50:
            return "warning"
        return "critical"