from flask import Flask, Response, render_template
from brands.brand_routes import BRANDS
from device.device_routes import DEVICE
from forum import FORUM
from user.user_routes import USER
from .config import Config
from api.api_routes import API

app: Flask = Flask(__name__, template_folder="templates")
app.config.from_object(Config())


def register_blueprints():
  app.register_blueprint(BRANDS)
  app.register_blueprint(DEVICE)
  app.register_blueprint(USER)
  app.register_blueprint(API)
  app.register_blueprint(FORUM)


register_blueprints()


@app.route('/')
def hello_page() -> Response:
  return render_template('index.html')
