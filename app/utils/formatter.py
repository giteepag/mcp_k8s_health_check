def extract_value(result):
    """
    Extracts single numeric value from Prometheus response.
    Handles empty / error-safe cases.
    """
    try:
        if not result or len(result) == 0:
            return None

        value = result[0].get("value", None)
        if not value:
            return None

        return float(value[1])

    except Exception:
        return None