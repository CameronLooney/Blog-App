from flask import Flask
app = Flask(__name__)
from config import Config
app.config.from_object(Config)
print(app.config["SECRET_KEY"])
from app import routes