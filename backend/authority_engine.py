# authority_engine.py

def resolve_authority(authority: str) -> dict:
    """
    Maps AI authority decision to real-world response units
    """

    authority_map = {
        "police": {
            "unit": "Police Control Room",
            "contact": "112",
            "department": "Law Enforcement"
        },
        "ambulance": {
            "unit": "Emergency Medical Services",
            "contact": "108",
            "department": "Medical Response"
        },
        "fire_brigade": {
            "unit": "Fire Department",
            "contact": "101",
            "department": "Fire & Rescue"
        },
        "disaster_response": {
            "unit": "National Disaster Response Force",
            "contact": "112",
            "department": "Disaster Management"
        },
        "rescue_team": {
            "unit": "Rescue Operations Unit",
            "contact": "112",
            "department": "Rescue Services"
        },
        "manual_review": {
            "unit": "Human Control Center",
            "contact": "internal",
            "department": "Operations Team"
        }
    }

    return authority_map.get(authority, {
        "unit": "Human Control Center",
        "contact": "internal",
        "department": "Operations Team"
    })
