from app.services.prometheus_client import PrometheusClient
from app.utils.health_score import normalize

MEMORY_QUERY = """
100 * (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes))
"""


class MemoryHealthTool:
    def __init__(self):
        self.prom = PrometheusClient()

    def get_memory_usage(self):
        return self.prom.query_scalar(MEMORY_QUERY)

    def evaluate(self):
        raw = self.get_memory_usage()
        mem_usage = float(raw)

        score = normalize(
            value=mem_usage,
            warning=70,
            critical=90
        )

        return {
            "metric": "memory",
            "usage_percent": mem_usage,
            "score": score,
            "status": self._status(score)
        }

    def _status(self, score):
        if score > 80:
            return "healthy"
        elif score > 50:
            return "warning"
        return "critical"