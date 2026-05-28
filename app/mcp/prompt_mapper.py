def map_prompt_to_action(prompt: str) -> str:
    prompt = prompt.lower()

    if "cpu" in prompt:
        return "cpu_health"

    if "memory" in prompt:
        return "memory_health"

    if "namespace" in prompt:
        return "namespace_health"

    if "cluster" in prompt or "overall" in prompt:
        return "cluster_health"

    return "cluster_health"  # fallback