from flask import Blueprint

post_view = Blueprint(
    "post_view",
    __name__,
    template_folder="templates/post",
    static_folder="static",
    static_url_path="/static"
)