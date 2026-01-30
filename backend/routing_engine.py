def route_case(category, priority):
    if priority == "CRITICAL":
        return "IMMEDIATE_DISPATCH"

    if category in ["DISASTER", "FIRE"]:
        return "EMERGENCY_FORCE"

    if category in ["CRIME", "WOMEN_SAFETY", "CHILD_SAFETY"]:
        return "LAW_ENFORCEMENT"

    if category == "MEDICAL":
        return "MEDICAL_SERVICES"

    return "GENERAL_CONTROL"
