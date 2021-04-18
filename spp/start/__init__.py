from flask import Blueprint

bp = Blueprint('start', __name__, template_folder="templates/")

from spp.start import routes