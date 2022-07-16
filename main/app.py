from flask import Flask, Response, render_template

from docs.docs_routes import DOCS
from allegro.allegro_routes import ALLEGRO
from brands.brand_routes import BRANDS
from forum.forum_routes import FORUM
from device.device_routes import DEVICE
from user.user_routes import USER

from .config import Config

app: Flask = Flask(__name__, template_folder="templates")
app.config.from_object(Config())


def register_blueprints():
  app.register_blueprint(BRANDS)
  app.register_blueprint(DEVICE)
  app.register_blueprint(USER)
  app.register_blueprint(DOCS)
  app.register_blueprint(FORUM)
  app.register_blueprint(ALLEGRO)


register_blueprints()


@app.route('/')
def hello_page() -> str:
  return render_template('index.html')
