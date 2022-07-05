from allegro.utils.allegro_authorization import get_access_token
from . import ALLEGRO


@ALLEGRO.route('/')
def hello_page() -> str:
  return "xd"
