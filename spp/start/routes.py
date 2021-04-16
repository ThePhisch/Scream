from spp.start import bp

@bp.route('/')
def index():
    return "it worx!"