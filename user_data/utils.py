from firebase_admin import messaging
from core.firebase import firebase_admin
from geopy.geocoders import Nominatim



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



def send_to_device(registration_token, title, body, data=None):
    """
    Send a notification to a specific device
    
    Args:
        registration_token (str): The FCM token of the target device
        title (str): Notification title
        body (str): Notification body
        data (dict): Optional key-value pairs of data
    """
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        data=data or {},
        token=registration_token,
    )
    
    return messaging.send(message)


def get_address_from_coordinates(latitude, longitude):
        geolocator = Nominatim(user_agent="test_app_123456")
        location = geolocator.reverse((latitude, longitude), language='ar')
        if location:
            return location
        return None
