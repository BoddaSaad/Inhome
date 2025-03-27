from firebase_admin import messaging
from core.firebase import firebase_admin


def send_to_topic(topic, title, body, data=None):
    firebase_admin.get_app()
    
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        data=data or {},
        topic=topic
    )
    return messaging.send(message)