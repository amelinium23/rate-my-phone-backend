import json

from requests import post
from typing import Dict
from flask import current_app

AUTHORIZATION_ALLEGRO_TOKEN_URL = "https://allegro.pl/auth/oauth/token"


def get_access_token() -> Dict[str, str]:
 token_response: Dict[str, str] = {}
 try:
   data = {'grant_type': 'client_credentials'}
   client_id = current_app.config.get('ALLEGRO_CLIENT_ID', '')
   client_secret = current_app.config.get('ALLEGRO_CLIENT_SECRET', '')
   token_response = post(AUTHORIZATION_ALLEGRO_TOKEN_URL, data=data,
                           allow_redirects=False, auth=(client_id, client_secret))
   token_response: Dict[str, str] = json.loads(token_response.text)
   return token_response
 except Exception:
  return {}
