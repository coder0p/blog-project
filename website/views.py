from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Post
from . import db

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
def home():
    posts = Post.query.order_by(Post.date_created.desc()).all()
    return render_template("home.html",current_user=current_user, posts=posts)



@views.route("/post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        Category_ = request.form.get('Category')
        title = request.form.get('title')
        content = request.form.get('content')
       # new_post = Post(title =title, Category=Category, content=content)

        if not Category_ :
            flash('Input items cannot be empty', category='error')
        elif not title:
            flash('Input items cannot be empty', category='error')
        elif not content:
            flash('Input items cannot be empty', category='error')
        else:
            post = Post(title =title, category=Category_, content=content, user_id=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('posts.html')