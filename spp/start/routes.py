from flask import render_template
from spp.start import bp

@bp.route('/')
def index():
    return render_template("index.html") 