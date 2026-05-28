def normalize(value: float, warning: float, critical: float) -> float:
    """
    Converts raw metric into 0–100 score.
    Higher = better health.
    """
    if value >= critical:
        return 0
    if value <= warning:
        return 100

    # linear interpolation between warning and critical
    return 100 - ((value - warning) / (critical - warning)) * 100


def weighted_score(scores: dict, weights: dict) -> float:
    """
    Combine multiple scores into one health score.
    """
    total = 0
    weight_sum = 0

    for key, score in scores.items():
        w = weights.get(key, 1)
        total += score * w
        weight_sum += w

    return round(total / weight_sum, 2)