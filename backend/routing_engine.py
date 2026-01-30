from team_engine import select_team

def route_case(ai_result, location):
    team = select_team(ai_result["type"], ai_result["severity"])

    return {
        "case_id": "NF-PS3-001",
        "type": ai_result["type"],
        "severity": ai_result["severity"],
        "priority": ai_result["priority"],
        "risk": ai_result["risk"],
        "location": location,
        "assigned_team": team,
        "status": "ASSIGNED",
        "eta": "7 minutes"
    }
