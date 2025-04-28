from flask_login import LoginManager, current_user
from views import user_view, index_view
from flask import redirect, url_for
from models import User, Post, Comment, db
from functools import wraps

login_manager = LoginManager()

def init_login(app):
    login_manager.init_app(app)
    login_manager.login_view = "user_view.login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("user_view.login"))
        elif not current_user.is_admin():
            return redirect(url_for("index_view.index"))
        return f(*args, **kwargs)
    return decorated_function

def author_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        
        if not current_user.is_authenticated:
            return redirect(url_for("user_view.login"))
        
        comment_id = kwargs.get("comment_id")
        post_id = kwargs.get("post_id")
        
        if not post_id and comment_id:
            comment = db.session.get(Comment, comment_id)
            if comment:
                post_id = comment.post_id
        
        post = db.session.get(Post, post_id)
        
        if not post:
            return redirect(url_for("index_view.index"))

        if post.users.id != current_user.id:
            return redirect(url_for("index_view.index"))
        
        return f(*args, **kwargs)
    return decorated_function

def author_or_admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        
        if not current_user.is_authenticated:
            return redirect(url_for("user_view.login"))
        
        comment_id = kwargs.get("comment_id")
        post_id = kwargs.get("post_id")
        
        if not post_id and comment_id:
            comment = db.session.get(Comment, comment_id)
            if comment:
                post_id = comment.post_id
        
        post = db.session.get(Post, post_id)
        if not post:
            return redirect(url_for("index_view.index"))

        if not (post.users.id == current_user.id or current_user.is_authenticated and current_user.is_admin()):
            return redirect(url_for("index_view.index"))

        return f(*args, **kwargs)
    return decorated_function