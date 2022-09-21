from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Post,Comment
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


@views.route("/delete/<int:id>/ ")
@login_required
def delete_post(id):
    
    post_to_delete = Post.query.filter_by(id=id).first_or_404( )
    id = current_user.id
    if id == post_to_delete.user_id:

        db.session.delete(post_to_delete)
        db.session.commit()
        flash("post deleted",category='success')
    return redirect (url_for('views.home'))


@views.route("/viewpost/<int:id>/", methods=['GET', 'POST'])
def view_post(id):
    
    post_view = Post.query.filter_by(id=id).all()
    
    return render_template("view_post.html",current_user=current_user, post_view=post_view)


@views.route("/comment/<int:id>", methods=['GET', 'POST'])
def comments(id):
    post_view = Post.query.filter_by(id=id).all()
    if request.method == "POST":
        print('yahooo')
        guestname = request.form.get('name')
        Comment_ = request.form.get('comment')
        print('jhvjgfj')
        if not guestname :
            flash('guest items cannot be empty', category='error')
        elif not Comment_:
            flash('comment items cannot be empty', category='error')
        else:
            print('dfgdbdgbhf')
            post = Comment(guestname =guestname, Comment=Comment_, post_id=id)
            db.session.add(post)
            db.session.commit()
            flash('commented........!', category='success')    
            return redirect(url_for("views.view_post",id = id ))
    else:
        flash("its not working")
    return render_template("view_post.html" ,post_view = post_view)
