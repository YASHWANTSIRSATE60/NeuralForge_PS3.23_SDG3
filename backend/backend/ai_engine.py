def analyze_emergency(message):
    msg = message.lower()

    if "collapse" in msg or "building" in msg or "earthquake" in msg:
        return {
            "type": "Structural Collapse",
            "severity": 5,
            "priority": "CRITICAL",
            "risk": "Life-threatening"
        }

    if "fire" in msg:
        return {
            "type": "Fire Accident",
            "severity": 4,
            "priority": "HIGH",
            "risk": "Severe"
        }

    if "flood" in msg:
        return {
            "type": "Flood",
            "severity": 3,
            "priority": "MEDIUM",
            "risk": "Moderate"
        }

    if "accident" in msg:
        return {
            "type": "Road Accident",
            "severity": 4,
            "priority": "HIGH",
            "risk": "Severe"
        }

    return {
        "type": "General Emergency",
        "severity": 2,
        "priority": "LOW",
        "risk": "Low"
    }
