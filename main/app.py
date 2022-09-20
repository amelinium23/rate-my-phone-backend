from flask import Flask, render_template
from main.utils.mixins import create_app, register_blueprints

rate_my_phone_app: Flask = create_app()
register_blueprints(rate_my_phone_app)


@rate_my_phone_app.route("/")
def hello_page() -> str:
  return render_template("index.html")
