from flask import Blueprint, request, jsonify, abort
from .models import db, Post
from datetime import datetime, timezone

post_api = Blueprint("post_api", __name__)

@post_api.route('/api/v1/posts', methods=['GET'])
def get_posts():
    posts = Post.query.filter_by(deleted_at=None).order_by(Post.id.desc()).all()    # deleted_at이 없는 게시글 전체 출력
    return jsonify([post.to_dict() for post in posts])

@post_api.route('/api/v1/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.deleted_at:
        abort(404)  # 해당 에러 출력
    return jsonify(post.to_dict())

@post_api.route('/api/v1/posts', methods=['POST'])
def create_post():
    data = request.get_json()   # 요청 본문에서 JSON 데이터 추출
    if not data or 'title' not in data or 'content' not in data:
        abort(400)
    new_post = Post(title=data['title'],
                    content=data['content'], 
                    created_at=datetime.now(timezone.utc))
    db.session.add(new_post)    # 대상 객체를 세션에 추가
    db.session.commit() # DB에 반영
    return jsonify(new_post.to_dict()), 201 # 저장된 게시글을 JSON으로 반환

@post_api.route('/api/v1/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.deleted_at:
        abort(404)
    data = request.get_json()
    post.title = data.get('title', post.title)
    post.content = data.get('content', post.content)
    post.updated_at = datetime.now(timezone.utc)
    db.session.commit()
    return jsonify(post.to_dict())

@post_api.route('/api/v1/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.deleted_at:
        abort(404)
    post.deleted_at = datetime.now(timezone.utc)
    db.session.commit()
    return jsonify({'message': 'deleted'})