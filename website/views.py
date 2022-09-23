from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Post,Comment,Category
from . import db

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
def home():
    posts = Post.query.order_by(Post.date_created.desc()).all()
    category = Category.query.all()
    return render_template("home.html",current_user=current_user, posts=posts,category=category)




@views.route("/post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        cat = request.form.get('Category')
        title = request.form.get('title')
        content = request.form.get('content')
        if not cat :
            flash('Input items cannot be empty', category='error')
        elif not title:
            flash('Input items cannot be empty', category='error')
        elif not content:
            flash('Input items cannot be empty', category='error')
        else:
            category = Category.query.filter_by(category = cat).first()
            if category:
                post = Post(title =title,category = category ,content=content, user_id=current_user.id)
            else:
                category = Category(category = cat,cat_user =current_user.id )
                db.session.add(category)
                db.session.commit()
                post = Post(title =title,category = category, content=content, user_id=current_user.id)
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
    comments_ = Comment.query.filter_by(post_id=id).order_by(Comment.date_created.desc()).all()
 
    return render_template("view_post.html",current_user=current_user, post_view=post_view,mycomment=comments_)


@views.route("/comment/<int:id>", methods=['GET','POST'])
def comments(id):
    post_view = Post.query.filter_by(id=id).all()
    if request.method == "POST":
        guestname = request.form.get('name')
        Comment_ = request.form.get('comment')
        
        if current_user.is_authenticated:
            if not Comment_:
                flash('comment section cannot be empty', category='error')
                return redirect(url_for('views.view_post',id=id))
        else:
            if not guestname :
                flash('name section cannot be empty', category='error')
                return redirect(url_for('views.view_post',id=id))
            if not Comment_:
                flash('comment section cannot be empty', category='error')
                return redirect(url_for('views.view_post',id=id))
            
        if current_user.is_authenticated:
            post = Comment(guestname =current_user.username, Comment=Comment_, post_id=id)                
        else:
            post = Comment(guestname =guestname, Comment=Comment_, post_id=id)
        db.session.add(post)
        db.session.commit()
        flash(f'{post.guestname} commented!', category='success')
        return redirect(url_for('views.view_post',id=id))
        
    return render_template('view_post.html',post_view=post_view)


@views.route("/category", methods=['GET','POST'])
@login_required
def add_category():
    if request.method == "POST":
        cat = request.form.get('category')
        if not cat :
            flash('Input items cannot be empty', category='error')
        else:
            category = Category(category = cat,cat_user =current_user.id )
            db.session.add(category)    
            db.session.commit()
            flash("category added..")
            return redirect(url_for('views.home'))
    return render_template('home.html')

    

@views.route("/category_del/<int:id>/", methods=['GET','POST'])
@login_required
def del_category(id):
    cat =  Category.query.filter_by(id=id).first()
    if request.method == "POST":
        print("thh")
        if not cat :
            flash('Input items cannot be empty', category='error')
        else:
            print(cat.cat_user)
            if current_user.id == cat.cat_user:
                db.session.delete(cat)    
                db.session.commit()
                flash("category added..")
            else:
                flash('jhdvcjhad')
            return redirect(url_for('views.home'))
    print("dasdas")
    return render_template('home.html')
