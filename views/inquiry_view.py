from flask import Blueprint, render_template, request, redirect, url_for
from models import *
from flask_login import login_required, current_user
from datetime import datetime, timezone
from auth import author_required, author_or_admin_required

inquiry_view = Blueprint(
    "inquiry_view",
    __name__,
    template_folder="../templates/post",
    static_folder="static",
    static_url_path="/static"
)

# Inquiry

@inquiry_view.route("/", methods=['GET'])
def inquiry():
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    keyword = request.args.get('keyword', '', type=str)
    search_type = request.args.get('type', 'title', type=str)
    
    stmt = db.select(Status).where(Status.name=="문의")
    status = db.session.execute(stmt).scalars().first()
    
    stmt = db.select(Post).where(Post.status_id == status.id).order_by(Post.created_at.desc())
    
    if keyword:
        if search_type == 'title':
            stmt = stmt.where(Post.title.contains(keyword))
        elif search_type == 'author':
            stmt = stmt.where(Post.users.has(User.username.contains(keyword)))
    
    posts = db.paginate(stmt, page=page, per_page=per_page, error_out=False)
    
    return render_template("inquiry/list.html", posts=posts)

@inquiry_view.route("/write", methods=['GET', 'POST'])
@login_required
def inquiry_wirte():
    
    error = None
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        if not title or not content:
            error='제목과 내용을 모두 입력하세요.'
        else:
            stmt = db.select(Status).where(Status.name=="문의")
            status = db.session.execute(stmt).scalars().first()
            
            new_post = Post(user_id = current_user.id, title=title, content=content, status_id=status.id)
            db.session.add(new_post)
            db.session.commit()
            
            return redirect(url_for("inquiry_view.inquiry"))
    
    return render_template("inquiry/write.html", error=error)

@inquiry_view.route("/<int:post_id>", methods=['GET'])
@author_or_admin_required
def inquiry_detail(post_id):
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    stmt = db.select(Post).where(Post.id==post_id)
    post = db.session.execute(stmt).scalars().first()
    
    stmt = db.select(Comment).where(Comment.post_id==post_id, Comment.status_id==post.status_id).order_by(Comment.created_at.desc())
    comments = db.paginate(stmt, page=page, per_page=per_page, error_out=False)
    
    post.readcnt += 1
    db.session.commit()
    
    return render_template("inquiry/detail.html", post=post, comments=comments, user=current_user)

@inquiry_view.route("/update/<int:post_id>", methods=['GET', 'POST'])
@author_required
def inquiry_update(post_id):
    
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
            return redirect(url_for("inquiry_view.inquiry_detail",  post_id=post_id))
    
    return render_template("inquiry/update.html", error=error, post=post)

@inquiry_view.route("/delete/<int:post_id>", methods=['GET', 'POST'])
@author_required
def inquiry_delete(post_id):
    
    stmt = db.select(Post).where(Post.id==post_id)
    post = db.session.execute(stmt).scalars().first()
    
    if request.method == 'POST':
        
        stmt = db.select(Status).where(Status.name=="삭제")
        status = db.session.execute(stmt).scalars().first()
        
        post.status_id = status.id
        
        stmt = db.select(Comment).where(Comment.post_id==post_id)
        comments = db.session.execute(stmt).scalars().all()
        
        for comment in comments:
            comment.status_id = status.id
        
        db.session.commit()
        
        return redirect(url_for("inquiry_view.inquiry"))
        
    return render_template("inquiry/delete.html", post_id=post_id)

@inquiry_view.route("/comment/<int:post_id>", methods=['GET', 'POST'])
@author_or_admin_required
def inquiry_comment(post_id):
    
    error = None
    
    user = current_user if current_user.is_authenticated else None
    
    if request.method == 'POST':
        content = request.form.get('content')
        if not content:
            error='내용을 입력하세요.'
        else:
            stmt = db.select(Status).where(Status.name=="문의")
            status = db.session.execute(stmt).scalars().first()
            
            new_comment =  Comment(user_id=current_user.id, post_id=post_id, content=content, status_id=status.id)
            db.session.add(new_comment)
            db.session.commit()
            
            return redirect(url_for("inquiry_view.inquiry_detail", post_id=post_id))
        
    return render_template("inquiry/comment.html", post_id=post_id, user=user, error=error)

@inquiry_view.route("/delete/comment/<int:comment_id>", methods=['GET', 'POST'])
@author_or_admin_required
def inquiry_comment_delete(comment_id):
    
    post_id = request.args.get('post_id', type=int)
    
    if request.method == 'POST':
        
        stmt = db.select(Status).where(Status.name=="삭제")
        status = db.session.execute(stmt).scalars().first()
        
        stmt = db.select(Comment).where(Comment.id == comment_id)
        comment = db.session.execute(stmt).scalars().first()
        
        comment.status_id = status.id
        db.session.commit()
        
        return redirect(url_for("inquiry_view.inquiry_detail", post_id = post_id))
    
    return render_template("inquiry/delete.html", post_id = post_id)

