from flask import Blueprint

api = Blueprint('api_1_0', __name__, template_folder="templates", static_folder="static")

from . import register, verify
