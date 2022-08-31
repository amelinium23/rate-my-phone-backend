import os
from google.cloud import storage
from firebase_admin import initialize_app, credentials, App, firestore

firebase_app: App = initialize_app(
    credentials.Certificate(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
)
db = firestore.client()
google_cloud_client = storage.Client()


def get_firebase_app():
    return firebase_app


def get_firestore_db():
    return db


def get_google_cloud_client():
    return google_cloud_client
