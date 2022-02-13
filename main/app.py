from flask import Flask, Response
from brands.brand_routes import BRANDS
from .config import DevelopmentConfig

app = Flask(__name__)

app.config.from_object(DevelopmentConfig())

app.register_blueprint(BRANDS)


@app.route('/')
def hello_page() -> Response:
  return Response('Welcome to rate my phone api!', status=200)
