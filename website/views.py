from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
#@login_required
def home():
    return render_template("home.html",current_user=current_user)


@views.route("/post")
@login_required
def post():
    return render_template("posts.html",current_user=current_user)