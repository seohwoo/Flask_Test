from flask import Blueprint, render_template, request, redirect, url_for
from models import *
from flask_login import login_required, current_user
from auth import admin_required, author_required
from datetime import datetime, timezone
#from sqlalchemy import select

notice_view = Blueprint(
    "notice_view",
    __name__,
    template_folder="../templates/post/notice",
    static_folder="static",
    static_url_path="/static"
)

# Notice

@notice_view.route("/", methods=['GET'])
def notice():
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 1, type=int)
    keyword = request.args.get('keyword', '', type=str)
    search_type = request.args.get('type', 'title', type=str)
    
    user = current_user if current_user.is_authenticated else None
        
    stmt = db.select(Status).where(Status.name == "공지")
    status = db.session.execute(stmt).scalars().first()
    
    stmt = db.select(Post).where(Post.status_id == status.id).order_by(Post.created_at.desc())
    
    if keyword:
        if search_type == 'title':
            stmt = stmt.where(Post.title.contains(keyword))
        elif search_type == 'author':
            stmt = stmt.where(Post.users.has(User.username.contains(keyword)))
    
    posts = db.paginate(stmt, page=page, per_page=per_page, error_out=False)
    
    return render_template("list.html", posts=posts, user=user)

@notice_view.route("/write", methods=['GET', 'POST'])
@admin_required
def notice_wirte():
    
    error = None
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        if not title or not content:
            error='제목과 내용을 모두 입력하세요.'
        else:
            
            stmt = db.select(Status).where(Status.name == "공지")
            status = db.session.execute(stmt).scalars().first()
            new_post = Post(user_id=current_user.id, title=title, content=content, status_id=status.id)
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for("notice_view.notice"))
    
    return render_template("notice/write.html", error=error)

@notice_view.route("/<int:post_id>", methods=['GET'])
def notice_detail(post_id):
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    user = current_user if current_user.is_authenticated else None
    
    stmt = db.select(Post).where(Post.id == post_id)
    post = db.session.execute(stmt).scalars().first()
    
    stmt = db.select(Comment).where(Comment.post_id==post_id, Comment.status_id==post.status_id).order_by(Comment.created_at.desc())
    comments = db.paginate(stmt, page=page, per_page=per_page, error_out=False)
    
    post.readcnt += 1
    db.session.commit()
    
    return render_template("notice/detail.html", post=post, comments=comments, user=user)

@notice_view.route("/update/<int:post_id>", methods=['GET', 'POST'])
@admin_required
def notice_update(post_id):
    
    error = None
    
    stmt = db.select(Post).where(Post.id==post_id)
    post = db.session.execute(stmt).scalars().first()
    
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

@notice_view.route("/delete/<int:post_id>", methods=['GET', 'POST'])
@admin_required
def notice_delete(post_id):
        
    if request.method == 'POST':
        
        stmt = db.select(Post).where(Post.id == post_id)
        post = db.session.execute(stmt).scalars().first()
        
        stmt = db.select(Status).where(Status.name == "삭제")
        status = db.session.execute(stmt).scalars().first()
        
        post.status_id = status.id
        
        stmt = db.select(Comment).where(Comment.post_id==post_id)
        comments = db.session.execute(stmt).scalars().all()
        for comment in comments:
            comment.status_id = status.id
        
        db.session.commit()
        return redirect(url_for("notice_view.notice"))
    
    return render_template("notice/delete.html", post_id=post_id)

@notice_view.route("/comment/<int:post_id>", methods=['GET', 'POST'])
@login_required
def notice_comment(post_id):
    
    error = None
    
    user = current_user if current_user.is_authenticated else None
    
    if request.method == 'POST':
        content = request.form.get('content')
        if not content:
            error='내용을 입력하세요.'
        else:
            stmt = db.select(Status).where(Status.name == "공지")
            status = db.session.execute(stmt).scalars().first()
            new_comment =  Comment(user_id=current_user.id, post_id=post_id, content=content, status_id=status.id)
            db.session.add(new_comment)
            db.session.commit()
            return redirect(url_for("notice_view.notice_detail", post_id=post_id))
        
    return render_template("notice/comment.html", user=user, post_id=post_id, error=error)

@notice_view.route("/delete/comment/<int:comment_id>", methods=['GET', 'POST'])
@author_required
def notice_comment_delete(comment_id):
    
    post_id = request.args.get('post_id', type=int)
    
    if request.method == 'POST':
        
        stmt = db.select(Status).where(Status.name=="삭제")
        status = db.session.execute(stmt).scalars().first()
        
        stmt = db.select(Comment).where(Comment.id==comment_id)
        comment = db.session.execute(stmt).scalars().first()
        
        comment.status_id = status.id
        db.session.commit()
        
        return redirect(url_for("notice_view.notice_detail", post_id = post_id))

    return render_template("notice/delete.html", post_id = post_id)
