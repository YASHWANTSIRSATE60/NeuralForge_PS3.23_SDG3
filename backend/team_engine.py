def assign_team(category):
    mapping = {
        "MEDICAL": "Ambulance + Hospital Team",
        "FIRE": "Fire Brigade Unit",
        "CRIME": "Police Unit",
        "DISASTER": "NDRF / SDRF Team",
        "WOMEN_SAFETY": "Women Safety Cell",
        "CHILD_SAFETY": "Child Protection Unit",
        "ACCIDENT": "Rescue + Ambulance",
        "INFRASTRUCTURE": "Municipal Emergency Team",
        "GENERAL": "Local Control Room"
    }

    return mapping.get(category, "Local Control Room")
