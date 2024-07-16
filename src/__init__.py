from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import dotenv_values
from account.routes import account_bp


app = Flask(__name__)
config = dotenv_values(".env")

# db
# login manager

app.register_blueprint(account_bp, url_prefix="/")