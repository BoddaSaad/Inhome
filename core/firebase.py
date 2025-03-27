import firebase_admin
from firebase_admin import credentials
from django.conf import settings

_firebase_app = None

def get_firebase_app():
    global _firebase_app
    if not _firebase_app:
        cred = credentials.Certificate(settings.FCM_CREDENTIAL_PATH)
        _firebase_app = firebase_admin.initialize_app(cred)
    return _firebase_app