import os
from allegro.utils.allegro_authorization import get_access_token
from main.firebase.firebase_app import get_firebase_app, get_firestore_db


class Config:
  DEBUG = True
  DEVELOPMENT = True
  FIREBASE_APP = get_firebase_app()
  FIRESTORE = get_firestore_db()
  ALLEGRO_CLIENT_ID = os.environ.get('ALLEGRO_CLIENT_ID')
  ALLEGRO_CLIENT_SECRET = os.environ.get('ALLEGRO_CLIENT_SECRET')
  ALLEGRO_TOKEN_RESPONSE = get_access_token()
