import logging
from flask_apscheduler import APScheduler
from flask import Flask, render_template, jsonify
from flask_cors import CORS
from main.config import Config
from docs.docs_routes import DOCS
from allegro.allegro_routes import ALLEGRO
from brands.brand_routes import BRANDS
from forum.forum_routes import FORUM
from device.device_routes import DEVICE
from main.tasks.brand_task import brand_task
from main.tasks.devices_taks import device_task
from user.user_routes import USER


def register_blueprints(app: Flask) -> None:
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


def get_app_scheduler(app: Flask) -> APScheduler:
    scheduler = APScheduler(app=app)
    with app.app_context():
        scheduler.add_job(
            id="save_brands_to_db",
            func=lambda: brand_task(app),
            trigger="interval",
            seconds=3600,
            misfire_grace_time=900,
        )
        scheduler.add_job(
            id="save_devices_to_db",
            func=lambda: device_task(app),
            trigger="interval",
            seconds=3600,
            misfire_grace_time=900,
        )
    return scheduler


def setup_loggers() -> None:
    logging.getLogger("apscheduler").setLevel(logging.INFO)


def create_app() -> Flask:
    app: Flask = Flask(
        __name__, template_folder="../templates", static_folder="../static"
    )
    setup_loggers()
    app.config.from_object(Config())
    app.register_error_handler(404, not_found)
    app.register_error_handler(500, internal_error)
    CORS(app, resource={r"/*/*": {"origins": "*"}, r"/*": {"origins": "*"}})
    scheduler = get_app_scheduler(app)
    scheduler.start()
    logging.getLogger(__name__).info(
        f"[SCHEDULER]: Scheduled jobs: {scheduler.get_jobs()}"
    )
    return app
