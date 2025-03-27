import firebase_admin
from firebase_admin import credentials
import os
from django.conf import settings

# Path to the Firebase credentials file
cred_path = settings.FIREBASE_CREDENTIALS_PATH
cred = credentials.Certificate(cred_path)

# Initialize Firebase app
if not firebase_admin._apps:  # Prevent re-initialization
    firebase_admin.initialize_app(cred)