import os
from typing import Any, Dict
from google.cloud.storage import Client as CloudClient
from google.cloud.firestore import Client as FirestoreClient
from firebase_admin import initialize_app, App, firestore, auth
from firebase_admin.credentials import Certificate


firebase_app: App = initialize_app(
    Certificate(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
)
db: FirestoreClient = firestore.client()
google_cloud_client: CloudClient = CloudClient()


def get_firebase_app() -> App:
    return firebase_app


def get_firestore_db() -> FirestoreClient:
    return db


def get_google_cloud_client() -> CloudClient:
    return google_cloud_client


def verify_token(token: str) -> Dict[str, Any]:
    return auth.verify_id_token(token)
