from flask import Blueprint

bp = Blueprint('start', __name__)

from spp.start import routes