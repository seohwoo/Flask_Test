from flask_login import LoginManager
from views import user_view
from flask import redirect
from models import User

login_manager = LoginManager()

def init_login(app):
    login_manager.init_app(app)
    login_manager.login_view = "user_view.login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))