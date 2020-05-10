from flask import Flask
from config import Config
from flask_login import LoginManager

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialise app object
app = Flask(__name__)
app.config.from_object(Config)
# Initialise login manager
login = LoginManager(app)
login.login_view = 'login'
# Initialise database object
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models