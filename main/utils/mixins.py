from flask import Flask, render_template, jsonify
from flask_cors import CORS
from main.config import Config
from docs.docs_routes import DOCS
from allegro.allegro_routes import ALLEGRO
from brands.brand_routes import BRANDS
from forum.forum_routes import FORUM
from device.device_routes import DEVICE
from user.user_routes import USER


def register_blueprints(app: Flask):
    app.register_blueprint(BRANDS)
    app.register_blueprint(DEVICE)
    app.register_blueprint(USER)
    app.register_blueprint(DOCS)
    app.register_blueprint(FORUM)
    app.register_blueprint(ALLEGRO)


def not_found(e):
  return render_template("404.html"), 404


def internal_error(e):
  return jsonify({"error": str(e)}), 500


def create_app() -> Flask:
    app: Flask = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(Config())
    app.register_error_handler(404, not_found)
    app.register_error_handler(500, internal_error)
    CORS(app, resource={r"/*": {"origins": "*"}})
    return app
