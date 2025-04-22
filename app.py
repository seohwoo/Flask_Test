from flask import Flask, request, jsonify, abort, render_template, redirect, url_for
from models import db
from models.post import Post
from datetime import datetime, timezone
import os
import requests

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///board.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    # SQLAlchemy에서 객체 변경 추적 기능을 비활성화

db.init_app(app)

# DB 초기화 (최초 실행 시만 생성)
if not os.path.exists('board.db'):
    with app.app_context():
        db.create_all()
        

# VIEW

@app.route('/')
def index():
    try:
        response = requests.get('http://localhost:5000/api/v1/posts')
        response.raise_for_status() # 응답이 실패하면 예외를 발생시킴
        posts = response.json() # JSON을 Python 객체(list of dicts)로 변환
    except requests.RequestException:
        posts = []

    return render_template('index.html', posts=posts)

@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':
        title = request.form.get('title')   # HTML 폼에서 입력된 제목과 내용을 받아옴
        content = request.form.get('content')
        if not title or not content:
            return render_template('write.html', error='제목과 내용을 모두 입력하세요.')

        try:
            response = requests.post(
                'http://localhost:5000/api/v1/posts',
                json={'title': title, 'content': content}
            )
            response.raise_for_status() 
            return redirect(url_for('index'))
        except requests.RequestException:
            return render_template('write.html', error='게시글 등록 중 오류가 발생했습니다.')

    return render_template('write.html')

@app.route('/<int:post_id>', methods=['GET'])
def detail(post_id):
    try:
        response = requests.get(f'http://localhost:5000/api/v1/posts/{post_id}')
        response.raise_for_status() 
        post = response.json()
    except requests.RequestException:
        post = []
    return render_template('detail.html', post=post)

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    try:
        response = requests.get(f'http://localhost:5000/api/v1/posts/{post_id}')
        response.raise_for_status() 
        post = response.json() 
    except requests.RequestException:
        post = []
    
    if request.method == 'POST':
        title = request.form.get('title')   
        content = request.form.get('content')
        if not title or not content:
            return render_template('update.html', post = post, error='제목과 내용을 모두 입력하세요.')

        try:
            response = requests.put(
                f'http://localhost:5000/api/v1/posts/{post_id}',
                json={'title': title, 'content': content}
            )
            response.raise_for_status() 
            return redirect(url_for('detail', post_id=post_id))
        except requests.RequestException:
            return render_template('update.html', post = post, error='게시글 수정 중 오류가 발생했습니다.')

    return render_template('update.html', post = post)

@app.route('/delete/<int:post_id>', methods=['GET', 'POST'])
def delete(post_id): 
    if request.method == 'POST':
        try:
            response = requests.delete(
                f'http://localhost:5000/api/v1/posts/{post_id}')
            response.raise_for_status() 
            return redirect(url_for('index'))
        except requests.RequestException:
            return render_template('delete.html', id=post_id, error='게시글 삭제 중 오류가 발생했습니다.')

    return render_template('delete.html', id=post_id)

# API

@app.route('/api/v1/posts', methods=['GET'])
def get_posts():
    posts = Post.query.filter_by(deleted_at=None).order_by(Post.id.desc()).all()    # deleted_at이 없는 게시글 전체 출력
    return jsonify([post.to_dict() for post in posts])

@app.route('/api/v1/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.deleted_at:
        abort(404)  # 해당 에러 출력
    return jsonify(post.to_dict())  # 저장된 게시글을 JSON으로 반환

@app.route('/api/v1/posts', methods=['POST'])
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

@app.route('/api/v1/posts/<int:post_id>', methods=['PUT'])
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

@app.route('/api/v1/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.deleted_at:
        abort(404)
    post.deleted_at = datetime.now(timezone.utc)
    db.session.commit()
    return jsonify({'message': 'deleted'})

if __name__ == '__main__':
    app.run(debug=True)