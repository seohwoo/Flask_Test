from flask import Blueprint

user_view = Blueprint(
    "user_view",
    __name__,
    template_folder="templates/user",
    static_folder="static",
    static_url_path="/static"
)