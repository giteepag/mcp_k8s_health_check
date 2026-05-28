from app.tools.cpu_health import CPUHealthTool
from app.tools.memory_health import MemoryHealthTool
from app.utils.health_score import weighted_score


class ClusterHealthTool:
    def __init__(self):
        self.cpu = CPUHealthTool()
        self.mem = MemoryHealthTool()

    def evaluate(self):
        cpu = self.cpu.evaluate()
        mem = self.mem.evaluate()

        scores = {
            "cpu": cpu["score"],
            "memory": mem["score"]
        }

        weights = {
            "cpu": 0.6,
            "memory": 0.4
        }

        cluster_score = weighted_score(scores, weights)

        return {
            "cluster_score": cluster_score,
            "status": self._status(cluster_score),
            "breakdown": {
                "cpu": cpu,
                "memory": mem
            }
        }

    def _status(self, score):
        if score > 80:
            return "healthy"
        elif score > 50:
            return "warning"
        return "critical"