from app.tools.cpu_health import CPUHealthTool
from app.tools.memory_health import MemoryHealthTool
from app.tools.namespace_health import NamespaceHealthTool

cpu_tool = CPUHealthTool()
mem_tool = MemoryHealthTool()
ns_tool = NamespaceHealthTool()


def route_action(action: str):
    if action == "cpu_health":
        return cpu_tool.evaluate()

    if action == "memory_health":
        return mem_tool.evaluate()
    
    if action == "namespace_health":
        return ns_tool.evaluate()

    if action == "cluster_health":
        return {
            "cpu": cpu_tool.evaluate(),
            "memory": mem_tool.evaluate()
        }

    return {"error": "Unknown action"}