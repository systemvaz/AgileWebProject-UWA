import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('AWD_PROJECT_KEY') or 'dlaskjaskld3290432LKNlk4094'
    # Database config
    SQLALCHEMY_DATABASE_URI = os.environ.get('AWD_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'database/app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False