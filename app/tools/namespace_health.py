from app.services.prometheus_client import PrometheusClient
from app.utils.health_score import normalize, weighted_score


class NamespaceHealthTool:
    def __init__(self):
        self.client = PrometheusClient()

    def evaluate(self):
        mem_query = """
        sum by (namespace) (
            container_memory_working_set_bytes
        )
        """

        cpu_query = """
        sum by (namespace) (
            rate(container_cpu_usage_seconds_total[5m])
        ) * 100
        """

        mem_result = self.client.query_vector(mem_query)
        cpu_result = self.client.query_vector(cpu_query)

        # Convert CPU result into dict for quick lookup
        cpu_map = {
            item["metric"].get("namespace", "unknown"): float(item["value"][1])
            for item in cpu_result
        }

        namespaces = []

        for item in mem_result:
            namespace = item["metric"].get("namespace", "unknown")
            mem_value = float(item["value"][1])

            mem_mb = mem_value / (1024 * 1024)
            cpu_usage = cpu_map.get(namespace, 0.0)

            # scoring
            mem_score = normalize(mem_mb, warning=500, critical=1000)
            cpu_score = normalize(cpu_usage, warning=60, critical=90)

            total_score = weighted_score(
                {"cpu": cpu_score, "memory": mem_score},
                {"cpu": 0.5, "memory": 0.5}
            )

            namespaces.append({
                "namespace": namespace,
                "cpu_percent": round(cpu_usage, 2),
                "memory_mb": round(mem_mb, 2),
                "score": total_score,
                "status": self._status(total_score)
            })

        return {"namespaces": namespaces}

    def _status(self, score):
        if score > 80:
            return "healthy"
        elif score > 50:
            return "warning"
        return "critical"