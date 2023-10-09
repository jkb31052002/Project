from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def initialize_app():
    app_instance = Flask(__name__)

    app_instance.config['SECRET_KEY'] = 'secretkey'
    app_instance.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app_instance.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

    db.init_app(app_instance)

    my_login_manager = LoginManager()
    my_login_manager.init_app(app_instance)

    from .models import CustomerUser

    @my_login_manager.user_loader
    def load_user(user_id):
        return CustomerUser.query.get(int(user_id))

    from .routes import auth as auth_blueprint
    app_instance.register_blueprint(auth_blueprint)

    from .routes import routes as main_blueprint
    app_instance.register_blueprint(main_blueprint)

    return app_instance
