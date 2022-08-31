import os
from main.firebase.firebase_app import get_firebase_app, get_firestore_db, get_google_cloud_client


class Config:
    DEBUG = True
    DEVELOPMENT = True
    FIREBASE_APP = get_firebase_app()
    FIRESTORE = get_firestore_db()
    GOOGLE_CLOUD_CLIENT = get_google_cloud_client()
    ALLEGRO_CLIENT_ID = os.environ.get("ALLEGRO_CLIENT_ID")
    ALLEGRO_CLIENT_SECRET = os.environ.get("ALLEGRO_CLIENT_SECRET")
