from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Post, Status, User, Auth
from flask_login import login_required, current_user
from datetime import datetime, timezone

post_view = Blueprint(
    "post_view",
    __name__,
    template_folder="../templates/post",
    static_folder="static",
    static_url_path="/static"
)

# Notice

@post_view.route("/notice", methods=['GET'])
def notice():
    status = Status.query.filter_by(name="공지").first()
    posts = Post.query.filter_by(status_id=status.id).order_by(Post.created_at.desc()).all()
    return render_template("notice/list.html", posts=posts)


@post_view.route("/notice/write", methods=['GET', 'POST'])
@login_required
def notice_wirte():
    error = None
    admin = User.query.filter_by(id=current_user.id).first()
    is_admin = admin.id == Auth.query.filter_by(name="관리자").first().id
    if is_admin:
        if request.method == 'POST':
            title = request.form.get('title')
            content = request.form.get('content')
            if not title or not content:
                error='제목과 내용을 모두 입력하세요.'
            else:
                status = Status.query.filter_by(name="공지").first()
                new_post = Post(author=admin.username, title=title, content=content, status_id=status.id)
                db.session.add(new_post)
                db.session.commit()
                return redirect(url_for("post_view.notice"))
    else:
        return redirect(url_for("post_view.notice"))
    return render_template("notice/write.html", error=error)

@post_view.route("/notice/<int:post_id>", methods=['GET'])
def notice_detail(post_id):
    post = Post.query.filter_by(id=post_id).first()
    post.readcnt += 1
    db.session.commit()
    return render_template("notice/detail.html", post=post)

@post_view.route("/notice/update/<int:post_id>", methods=['GET', 'POST'])
@login_required
def notice_update(post_id):
    error = None
    admin = User.query.filter_by(id=current_user.id).first()
    is_admin = admin.auth_id == Auth.query.filter_by(name="관리자").first().id
    if is_admin:
        post = Post.query.filter_by(id=post_id).first()
        if request.method == 'POST':
            title = request.form.get('title')
            content = request.form.get('content')
            if not title or not content:
                error='제목과 내용을 모두 입력하세요.'
            else:
                post.title = title
                post.content = content
                post.updated_at = datetime.now(timezone.utc)
                db.session.commit()
                return redirect(url_for("post_view.notice_detail",  post_id=post_id))
    else:
        return redirect(url_for("post_view.notice_detail", post_id=post_id))
    return render_template("notice/update.html", error=error, post=post)

@post_view.route("/notice/delete/<int:post_id>", methods=['GET', 'POST'])
@login_required
def notice_delete(post_id):
    admin = User.query.filter_by(id=current_user.id).first()
    is_admin = admin.auth_id == Auth.query.filter_by(name="관리자").first().id
    if is_admin:
        post = Post.query.filter_by(id=post_id).first()
        if request.method == 'POST':
            status = Status.query.filter_by(name="삭제").first()
            post.status_id = status.id
            db.session.commit()
            return redirect(url_for("post_view.notice"))
    return render_template("notice/delete.html")


# # Inquiry


# @post_view.route("/inquiry", methods=['GET'])
# def inquiry():
#     status = Status.query.filter_by(name="문의").first()
#     posts = Post.query.filter_by(status_id=status.id).order_by(Post.created_at.desc()).all()
#     return render_template("inquiry/list.html", posts=posts)


# @post_view.route("/inquiry/write", methods=['GET', 'POST'])
# @login_required
# def inquiry_wirte():
#     error = None
#     author = User.query.filter_by(id=current_user.id).first()
#     if request.method == 'POST':
#         title = request.form.get('title')
#         content = request.form.get('content')
#         if not title or not content:
#             error='제목과 내용을 모두 입력하세요.'
#         else:
#             status = Status.query.filter_by(name="문의").first()
#             new_post = Post(author=author.username, title=title, content=content, status_id=status.id)
#             db.session.add(new_post)
#             db.session.commit()
#             return redirect(url_for("post_view.inquiry"))
#     return render_template("inquiry/write.html", error=error)

# @post_view.route("/inquiry/<int:post_id>", methods=['GET'])
# def inquiry_detail(post_id):
#     post = Post.query.filter_by(id=post_id).first()
#     post.readcnt += 1
#     db.session.commit()
#     return render_template("inquiry/detail.html", post=post)

# @post_view.route("/inquiry/update/<int:post_id>", methods=['GET', 'POST'])
# @login_required
# def inquiry_update(post_id):
#     error = None
#     author = User.query.filter_by(id=current_user.id).first()
#     post = Post.query.filter_by(id=post_id).first()
#     is_author = post.author == author.username
#     if is_author:
#         if request.method == 'POST':
#             title = request.form.get('title')
#             content = request.form.get('content')
#             if not title or not content:
#                 error='제목과 내용을 모두 입력하세요.'
#             else:
#                 post.title = title
#                 post.content = content
#                 post.updated_at = datetime.now(timezone.utc)
#                 db.session.commit()
#                 return redirect(url_for("post_view.inquiry_detail",  post_id=post_id))
#     else:
#         return redirect(url_for("post_view.inquiry_detail", post_id=post_id))
#     return render_template("inquiry/update.html", error=error, post=post)

# @post_view.route("/inquiry/delete/<int:post_id>", methods=['GET', 'POST'])
# @login_required
# def inquiry_delete(post_id):
#     author = User.query.filter_by(id=current_user.id).first()
#     post = Post.query.filter_by(id=post_id).first()
#     is_author = post.author == author.username
#     if is_author:
#         if request.method == 'POST':
#             status = Status.query.filter_by(name="삭제").first()
#             post.status_id = status.id
#             db.session.commit()
#             return redirect(url_for("post_view.inquiry"))
#     return render_template("inquiry/delete.html")