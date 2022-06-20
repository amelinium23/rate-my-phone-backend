import os
from firebase_admin import initialize_app, credentials


firebase_app = initialize_app(credentials.Certificate(os.getenv("GOOGLE_APPLICATION_CREDENTIALS")))


def get_firebase_app():
    return firebase_app
