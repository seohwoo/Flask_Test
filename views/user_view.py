from flask import Blueprint, redirect, render_template, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from models import User, Auth, db

user_view = Blueprint(
    "user_view",
    __name__,
    template_folder="../templates/user",
    static_folder="static",
    static_url_path="/static"
)

@user_view.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()

        if not username or not password:
            error='아이디와 비밀번호를 모두 입력하세요.'
        elif user and user.password == password:
            login_user(user)
            return redirect(url_for("index_view.index"))
        else:
            error = "아이디 또는 비밀번호를 확인해주세요."
    return render_template("login.html", error=error)

@user_view.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index_view.index"))

@user_view.route("/register", methods=['GET', 'POST'])
def reqister():
    
    if current_user.is_authenticated:
        return redirect(url_for("index_view.index"))
    
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        
        if not username or not password:
            error='아이디와 비밀번호를 모두 입력하세요.'
        elif user:
            error = "이미 사용중인 아이디입니다."
        else:
            auth = Auth.query.filter_by(name="사용자").first()
            new_user = User(username=username, password=password, auth_id=auth.id)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for("index_view.index"))
        
    return render_template("register.html", error=error)