import requests
from app.core.config import PROMETHEUS_URL


class PrometheusClient:
    def __init__(self):
        self.base_url = PROMETHEUS_URL

    def query_scalar(self, promql: str) -> float:
        """For single-value queries (CPU, memory)"""
        url = f"{self.base_url}/api/v1/query"
        response = requests.get(url, params={"query": promql})

        data = response.json()

        result = data["data"]["result"]

        if not result:
            return 0.0

        return float(result[0]["value"][1])

    def query_vector(self, promql: str) -> list:
        """For multi-series queries (namespace, pods)"""
        url = f"{self.base_url}/api/v1/query"
        response = requests.get(url, params={"query": promql})

        data = response.json()

        return data["data"]["result"]