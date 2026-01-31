def determine_routing(authority_key: str):
    routes = {
        "police": {
            "unit": "Police Control Room",
            "code": "PCR-100",
            "description": "Law enforcement and public safety"
        },
        "ambulance": {
            "unit": "Emergency Medical Services",
            "code": "EMS-108",
            "description": "Medical assistance and transport"
        },
        "fire_brigade": {
            "unit": "Fire Department",
            "code": "FD-101",
            "description": "Fire suppression and rescue"
        },
        "disaster_response": {
            "unit": "Disaster Response Force",
            "code": "NDRF-HQ",
            "description": "Large scale disaster management"
        },
        "rescue_team": {
            "unit": "Rescue Operations Unit",
            "code": "ROU-Alpha",
            "description": "Specialized rescue operations"
        }
    }
    
    # Normalize key
    key = authority_key.lower().replace(" ", "_")
    
    return routes.get(key, routes["police"]) # Default to police
