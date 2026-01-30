def select_team(emergency_type, severity):
    teams = [
        {"id": "T1", "type": "Fire Team", "status": "Available"},
        {"id": "T2", "type": "Medical Team", "status": "Available"},
        {"id": "T3", "type": "Disaster Response Team", "status": "Available"}
    ]

    if emergency_type == "Structural Collapse":
        return teams[2]

    if emergency_type == "Fire Accident":
        return teams[0]

    if emergency_type == "Road Accident":
        return teams[1]

    return teams[1]
