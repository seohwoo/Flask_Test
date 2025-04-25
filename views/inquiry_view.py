from flask import Blueprint, render_template, request, redirect, url_for
from models import *
from flask_login import login_required, current_user
from datetime import datetime, timezone

inquiry_view = Blueprint(
    "inquiry_view",
    __name__,
    template_folder="../templates/post",
    static_folder="static",
    static_url_path="/static"
)

# Inquiry

@inquiry_view.route("/inquiry", methods=['GET'])
def inquiry():
    
    status = Status.query.filter_by(name="문의").first()
    posts = Post.query.filter_by(status_id=status.id).order_by(Post.created_at.desc()).all()
    
    return render_template("inquiry/list.html", posts=posts)

@inquiry_view.route("/inquiry/write", methods=['GET', 'POST'])
@login_required
def inquiry_wirte():
    
    error = None
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        if not title or not content:
            error='제목과 내용을 모두 입력하세요.'
        else:
            status = Status.query.filter_by(name="문의").first()
            user = User.query.filter_by(id=current_user.id).first()
            new_post = Post(author=user.username, title=title, content=content, status_id=status.id)
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for("inquiry_view.inquiry"))
    
    return render_template("inquiry/write.html", error=error)

@inquiry_view.route("/inquiry/<int:post_id>", methods=['GET'])
@login_required
def inquiry_detail(post_id):
    
    post = Post.query.filter_by(id=post_id).first()
    user = User.query.filter_by(id=current_user.id).first()
    
    is_admin = user.id == Auth.query.filter_by(name="관리자").first().id
    username = user.username
    
    if not (is_admin or post.author == user.username):
        return redirect(url_for("inquiry_view.inquiry"))
    
    comments = Comment.query.filter_by(post_id=post_id, status_id = post.status_id).order_by(Comment.created_at.asc()).all()
    post.readcnt += 1
    db.session.commit()
    
    return render_template("inquiry/detail.html", post=post, comments=comments, username=username, is_admin=is_admin)

@inquiry_view.route("/inquiry/update/<int:post_id>", methods=['GET', 'POST'])
@login_required
def inquiry_update(post_id):
    
    error = None
    
    user = User.query.filter_by(id=current_user.id).first()
    post = Post.query.filter_by(id=post_id).first()
    
    is_author = user.username == post.author
    
    if not is_author:
        return redirect(url_for("inquiry_view.inquiry_detail", post_id=post_id))
    
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
            return redirect(url_for("inquiry_view.inquiry_detail",  post_id=post_id))
    
    return render_template("inquiry/update.html", error=error, post=post)

@inquiry_view.route("/inquiry/delete/<int:post_id>", methods=['GET', 'POST'])
@login_required
def inquiry_delete(post_id):
    
    user = User.query.filter_by(id=current_user.id).first()   
    post = Post.query.filter_by(id=post_id).first()
    
    if user.username != post.author:
        return redirect(url_for("inquiry_view.inquiry_detail", post_id=post_id))
    
    if request.method == 'POST':
        status = Status.query.filter_by(name="삭제").first()
        post.status_id = status.id
        
        comments = Comment.query.filter_by(post_id=post_id).all()
        for comment in comments:
            comment.status_id = status.id
        
        db.session.commit()
        return redirect(url_for("inquiry_view.inquiry"))
        
    return render_template("inquiry/delete.html", post_id=post_id)

@inquiry_view.route("/inquiry/comment/<int:post_id>", methods=['GET', 'POST'])
@login_required
def inquiry_comment(post_id):
    
    error = None
    
    user = User.query.filter_by(id=current_user.id).first()
    post = Post.query.filter_by(id=post_id).first()
    
    is_admin = user.id == Auth.query.filter_by(name="관리자").first().id
    
    if not (is_admin or user.username == post.author):
        return redirect(url_for("inquiry_view.inquiry_detail", post_id=post_id))
    
    if request.method == 'POST':
        content = request.form.get('content')
        if not content:
            error='내용을 입력하세요.'
        else:
            status = Status.query.filter_by(name="문의").first()
            new_comment =  Comment(author=user.username, post_id=post_id, content=content, status_id=status.id)
            db.session.add(new_comment)
            db.session.commit()
            return redirect(url_for("inquiry_view.inquiry_detail", post_id=post_id))
        
    return render_template("inquiry/comment.html", post_id=post_id, username = user.username, error=error)

@inquiry_view.route("/inquiry/delete/comment/<int:comment_id>", methods=['GET', 'POST'])
@login_required
def inquiry_comment_delete(comment_id):
    
    user = User.query.filter_by(id=current_user.id).first()
    comment = Comment.query.filter_by(id=comment_id).first()
    post = Post.query.filter_by(id=comment.post_id).first()
    
    if user.username != comment.author:
        return redirect(url_for("inquiry_view.inquiry_detail", post_id = post.id))
    
    if request.method == 'POST':
        status = Status.query.filter_by(name="삭제").first()
        comment.status_id = status.id
        db.session.commit()
        return redirect(url_for("inquiry_view.inquiry_detail", post_id = post.id))
    
    return render_template("inquiry/delete.html", post_id = post.id)

