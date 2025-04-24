from flask import Blueprint, render_template

index_view = Blueprint(
    "index_view",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/static"
)

@index_view.route("/")
def index():
    return render_template("index.html")