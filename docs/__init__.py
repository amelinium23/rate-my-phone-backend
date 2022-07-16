from flask import Blueprint

DOCS = Blueprint("docs", __name__, template_folder="templates",
                 url_prefix="/docs", static_folder="static")
