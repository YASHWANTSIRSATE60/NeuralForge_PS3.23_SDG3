AUTHORITY_MAP = {
    "MEDICAL": "Emergency Medical Services",
    "SAFETY": "Police Department",
    "DISASTER": "Disaster Response Authority",
    "CRIME": "Police Department",
    "INFRASTRUCTURE": "Municipal Corporation",
    "WOMEN_CHILD": "Women Safety Cell",
    "MENTAL_HEALTH": "Mental Health Helpline",
    "ANIMAL_RESCUE": "Animal Welfare Department",
    "PUBLIC_SERVICE": "Local Administration"
}

def resolve_authority(category):
    return AUTHORITY_MAP.get(category, "General Emergency Authority")
