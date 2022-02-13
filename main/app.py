from flask import Flask, Response
from brands.brand_routes import BRANDS
from device.device_routes import DEVICE
from .config import Config

app: Flask = Flask(__name__)

app.config.from_object(Config())

app.register_blueprint(BRANDS)
app.register_blueprint(DEVICE)

@app.route('/')
def hello_page() -> Response:
  return Response('Welcome to rate my phone api!', status=200)
