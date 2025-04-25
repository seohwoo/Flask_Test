from flask import Blueprint, render_template, request, redirect, url_for
from models import *
from flask_login import login_required, current_user
from datetime import datetime, timezone

notice_view = Blueprint(
    "notice_view",
    __name__,
    template_folder="../templates/post",
    static_folder="static",
    static_url_path="/static"
)

# Notice

@notice_view.route("/notice", methods=['GET'])
def notice():
    
    is_admin = None
    
    if current_user.is_authenticated:
        user = User.query.filter_by(id=current_user.id).first()
        is_admin = user.id == Auth.query.filter_by(name="관리자").first().id
        
    status = Status.query.filter_by(name="공지").first()
    posts = Post.query.filter_by(status_id=status.id).order_by(Post.created_at.desc()).all()
    return render_template("notice/list.html", posts=posts, is_admin=is_admin)

@notice_view.route("/notice/write", methods=['GET', 'POST'])
@login_required
def notice_wirte():
    
    error = None
    
    user = User.query.filter_by(id=current_user.id).first()
    is_admin = user.id == Auth.query.filter_by(name="관리자").first().id
    
    if not is_admin:
        return redirect(url_for("notice_view.notice"))
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        if not title or not content:
            error='제목과 내용을 모두 입력하세요.'
        else:
            status = Status.query.filter_by(name="공지").first()
            new_post = Post(author=user.username, title=title, content=content, status_id=status.id)
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for("notice_view.notice"))
    
    return render_template("notice/write.html", error=error)

@notice_view.route("/notice/<int:post_id>", methods=['GET'])
def notice_detail(post_id):
    
    is_admin = None
    username = None
    
    if current_user.is_authenticated:
        user = User.query.filter_by(id=current_user.id).first()
        is_admin = user.id == Auth.query.filter_by(name="관리자").first().id
        username = user.username
    
    post = Post.query.filter_by(id=post_id).first()
    comments = Comment.query.filter_by(post_id=post_id, status_id = post.status_id).order_by(Comment.created_at.asc()).all()
    post.readcnt += 1
    db.session.commit()
    
    return render_template("notice/detail.html", post=post, comments=comments, is_admin=is_admin, username=username)

@notice_view.route("/notice/update/<int:post_id>", methods=['GET', 'POST'])
@login_required
def notice_update(post_id):
    
    error = None
    
    user = User.query.filter_by(id=current_user.id).first()
    is_admin = user.auth_id == Auth.query.filter_by(name="관리자").first().id
    
    if not is_admin:
        return redirect(url_for("notice_view.notice_detail", post_id=post_id))
    
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
            return redirect(url_for("notice_view.notice_detail",  post_id=post_id))
    
    return render_template("notice/update.html", error=error, post=post)

@notice_view.route("/notice/delete/<int:post_id>", methods=['GET', 'POST'])
@login_required
def notice_delete(post_id):
    
    user = User.query.filter_by(id=current_user.id).first()
    is_admin = user.auth_id == Auth.query.filter_by(name="관리자").first().id
    
    if not is_admin:
        return redirect(url_for("notice_view.notice_detail", post_id=post_id))
        
    if request.method == 'POST':
        post = Post.query.filter_by(id=post_id).first()
        status = Status.query.filter_by(name="삭제").first()
        post.status_id = status.id
        
        comments = Comment.query.filter_by(post_id=post_id).all()
        for comment in comments:
            comment.status_id = status.id
        
        db.session.commit()
        return redirect(url_for("notice_view.notice"))
    
    return render_template("notice/delete.html", post_id=post_id)


@notice_view.route("/notice/comment/<int:post_id>", methods=['GET', 'POST'])
@login_required
def notice_comment(post_id):
    
    error = None
    
    user = User.query.filter_by(id=current_user.id).first()
    
    if request.method == 'POST':
        content = request.form.get('content')
        if not content:
            error='내용을 입력하세요.'
        else:
            status = Status.query.filter_by(name="공지").first()
            new_comment =  Comment(author=user.username, post_id=post_id, content=content, status_id=status.id)
            db.session.add(new_comment)
            db.session.commit()
            return redirect(url_for("notice_view.notice_detail", post_id=post_id))
        
    return render_template("notice/comment.html", post_id=post_id, username = user.username, error=error)

@notice_view.route("/notice/delete/comment/<int:comment_id>", methods=['GET', 'POST'])
@login_required
def notice_comment_delete(comment_id):
    
    comment = Comment.query.filter_by(id=comment_id).first()
    user = User.query.filter_by(id=current_user.id).first()
    
    if comment.author != user.username:
        return redirect(url_for("notice_view.notice_detail", post_id = comment.post_id))
    
    if request.method == 'POST':
        status = Status.query.filter_by(name="삭제").first()
        comment.status_id = status.id
        db.session.commit()
        return redirect(url_for("notice_view.notice_detail", post_id = comment.post_id))

    return render_template("notice/delete.html", post_id = comment.post_id)
