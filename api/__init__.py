from flask import Blueprint

API = Blueprint('api', __name__, template_folder="templates", url_prefix="/api")
