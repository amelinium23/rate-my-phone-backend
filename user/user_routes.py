from logging import Logger

from flask import Response
from . import USER

logger = Logger(__name__)


@USER.route('/user')
def get_user_by_id() -> Response:
  return "No tak"
