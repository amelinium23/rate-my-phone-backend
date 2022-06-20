from main.firebase.firebase_app import get_firebase_app


class Config:
  DEBUG = True
  DEVELOPMENT = True
  FIREBASE_APP = get_firebase_app()
