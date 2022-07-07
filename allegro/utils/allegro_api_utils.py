import json

from requests import get
from typing import Dict, Any

URL = "https://api.allegro.pl/"

DEFAULT_HEADERS = {
    'Accept': 'application/vnd.allegro.public.v1+json',
    'Authorization': '',
}


def search_listings_in_allegro(device_name: str, access_token: str) -> Dict[str, Any]:
 try:
  headers = _fill_headers_with_token(access_token)
  params = {'searchPhrase': device_name, 'parameter.11323': '11323_2'}
  response = get(URL.rstrip('/') + '/offers/listings', headers=headers,
                 params=params)
  return json.loads(response.text)
 except Exception as e:
  return {'error': str(e)}


def get_categories(access_token: str) -> Dict[str, Any]:
 try:
  headers = _fill_headers_with_token(access_token)
  response = get(URL.rstrip('/') + '/sale/categories', headers=headers)
  return json.loads(response.text)
 except Exception as e:
  return {'error': str(e)}


def get_categories_by_parent_id(access_token: str, parent_id: str) -> Dict[str, Any]:
  try:
    headers = _fill_headers_with_token(access_token)
    params = {'parent.id': parent_id}
    response = get(URL.rstrip('/') + '/sale/categories',
                   headers=headers, params=params)
    return json.loads(response.text)
  except Exception as e:
    return {'error': str(e)}


def _fill_headers_with_token(access_token: str, headers: Dict[str, str] = DEFAULT_HEADERS) -> Dict[str, str]:
 headers['Authorization'] = 'Bearer ' + access_token
 return headers
