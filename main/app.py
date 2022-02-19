from logging import Logger
from flask import Flask, Response
from brands.brand_routes import BRANDS
from device.device_routes import DEVICE
from user.user_routes import USER
from .config import Config

app: Flask = Flask(__name__)

logger: Logger = Logger(__name__)

app.config.from_object(Config())

app.register_blueprint(BRANDS)
app.register_blueprint(DEVICE)
app.register_blueprint(USER)


@app.route('/')
def hello_page() -> Response:
  """Index endpoint for api

  Returns:
      Response
  """
  return Response('Welcome to rate my phone api!')
