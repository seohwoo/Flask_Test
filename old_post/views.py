from flask import Blueprint, render_template

post_view = Blueprint(
    'post_view',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/post/static'
)

@post_view.route('/')
def index():
    return render_template('index.html')

@post_view.route('/write')
def write():
    return render_template('write.html')

@post_view.route('/<int:post_id>')
def detail(post_id):
    return render_template('detail.html')

@post_view.route('/update/<int:post_id>')
def update(post_id):
    return render_template('update.html')