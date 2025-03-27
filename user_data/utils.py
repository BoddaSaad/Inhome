from firebase_admin import messaging


def send_to_topic(topic, title, body, data=None):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        data=data or {},
        topic=topic
    )
    return messaging.send(message)