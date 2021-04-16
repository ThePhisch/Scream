from flask import Flask

def create_app():
    app = Flask(__name__)

    from spp.start import bp as starter_bp
    app.register_blueprint(starter_bp)

    return app