from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
app = Flask(__name__)
# is_authenticated: a property that is True if the user has valid credentials or False otherwise.
# is_active: a property that is True if the user’s account is active or False otherwise.
# is_anonymous: a property that is False for regular users, and True for a special, anonymous user.
# get_id(): a method that returns a unique identifier for the user as a string
login = LoginManager(app)
# app needs login view
login.login_view = 'login' # end point for login
from config import Config
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
from app import routes,models
