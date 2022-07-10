import json

from requests import post, Response
from typing import Dict
from flask import current_app

AUTHORIZATION_ALLEGRO_TOKEN_URL = "https://allegro.pl/auth/oauth/token"


def get_access_token() -> Dict[str, str]:
 try:
   data = {'grant_type': 'client_credentials'}
   client_id = current_app.config.get('ALLEGRO_CLIENT_ID', '')
   client_secret = current_app.config.get('ALLEGRO_CLIENT_SECRET', '')
   token_response: Response = post(AUTHORIZATION_ALLEGRO_TOKEN_URL, data=data,
                           allow_redirects=False, auth=(client_id, client_secret))
   parsed_response = token_response.json()
   return parsed_response
 except Exception:
  return {}
