from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import dotenv_values
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    config_env = dotenv_values(".env")
    app.config['SECRET_KEY'] = config_env['SECRET_KEY']
    app.config['SQLALCHEMY_DATABASE_URI'] = config_env['SQLALCHEMY_DATABASE_URI']

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'account.login'
    login_manager.init_app(app)

    from account.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from account.routes import account_bp
    from library.routes import library_bp

    app.register_blueprint(account_bp, url_prefix="/")
    app.register_blueprint(library_bp, url_prefix="/")
    # create_db(app)
    return app


def create_db(app):
    from account.models import User
    with app.app_context():
        db.create_all()
        print("Database created!")
