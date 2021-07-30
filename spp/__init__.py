from flask import Flask
from flask_login.login_manager import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = "start.unauthorised"
socketio = SocketIO()

def create_app(config_class=Config) -> SocketIO:
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    socketio.init_app(app)

    from spp.start import bp as starter_bp
    from spp.chat import bp as chatter_bp
    app.register_blueprint(starter_bp)
    app.register_blueprint(chatter_bp)

    
    return app