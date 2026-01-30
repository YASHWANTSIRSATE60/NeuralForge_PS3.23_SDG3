def send_notification(authority, message, location, priority):
    return {
        "sent_to": authority,
        "message": message,
        "location": location,
        "priority": priority,
        "status": "NOTIFIED"
    }
