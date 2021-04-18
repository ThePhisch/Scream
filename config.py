import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI') or \
        'sqlite:///' + os.path.join(basedir, 'scream.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE_USER = os.environ.get('DB_USER')
    DATABASE_PASS = os.environ.get('DB_PASS')