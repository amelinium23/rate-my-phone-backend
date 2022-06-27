import os
from firebase_admin import initialize_app, credentials, App, firestore


firebase_app: App = initialize_app(credentials.Certificate(
    os.getenv("GOOGLE_APPLICATION_CREDENTIALS")))
db = firestore.client()


def get_firebase_app():
  return firebase_app


def get_firestore_db():
  return db
