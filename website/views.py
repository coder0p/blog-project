from flask import Blueprint, render_template, request,Response, flash, redirect, url_for,jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .models import Post,Comment,Category,Like,Image
from . import db
from slugify import slugify


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
        slug=slugify(title)
        if not cat :
            flash('Input items cannot be empty', category='error')
        elif not title:
            flash('Input items cannot be empty', category='error')
        elif not content:
            flash('Input items cannot be empty', category='error')
        else:
            category = Category.query.filter_by(category = cat).first()
            if category:
                post = Post(title =title,category = category ,content=content, 
                            category_id=category.id,user_id=current_user.id,slug=slug)
            else:
                category = Category(category = cat,cat_user =current_user.id )
                db.session.add(category)
                db.session.commit()
                post = Post(title =title,category = category, content=content, user_id=current_user.id,slug=slug)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.home'))
    category = Category.query.all()
    return render_template('posts.html', categories = category)



@views.route("/viewpost/<int:id>/<slug>", methods=['GET', 'POST'])
def view_post(id,slug):
    slug_= slugify(slug,allow_unicode=True)
    if not slug:
        return redirect(url_for('views.views_post'))
    else:
        
        post_view = Post.query.filter_by(id=id).all() 
        post = db.session.query(Post).filter_by(slug = slug).first()

        comments_ = Comment.query.filter_by(post_id=id).order_by(Comment.date_created.desc()).all()
    

    return render_template("view_post.html",current_user=current_user,slug=slug_,
                               post_view=post_view,mycomment=comments_,post=post)


@views.route("/viewpost/<int:id>/", methods=['GET', 'POST'])
def views_post(id):
    post_view = Post.query.filter_by(id=id).all() 
    #post = db.session.query(Post).filter_by(slug = slug).first()
    comments_ = Comment.query.filter_by(post_id=id).order_by(Comment.date_created.desc()).all()

    return render_template("view_post.html",current_user=current_user,
                               post_view=post_view,mycomment=comments_)


   
@views.route("/delete/<int:id>/ ")
@login_required
def delete_post(id):
    post_to_delete = Post.query.filter_by(id=id).first_or_404()
    id = current_user.id
    if id == post_to_delete.user_id:
        db.session.delete(post_to_delete)
        db.session.commit()
        flash("post deleted",category='success')
    return redirect (url_for('views.home'))


# @views.route("/viewpost/<int:id>/", methods=['GET', 'POST'])
# def view_post(id):
#     post_view = Post.query.filter_by(id=id).all() 
#     comments_ = Comment.query.filter_by(post_id=id).order_by(Comment.date_created.desc()).all()
 
#     return render_template("view_post.html",current_user=current_user, post_view=post_view,mycomment=comments_)


@views.route("/comment/<int:id>/<slug>", methods=['GET','POST'])
def comments(id,slug):
    post_view = Post.query.filter_by(id=id).all()
    slug_= slugify(slug,allow_unicode=True)
   # slug_=slugify(slugs_.title,allow_unicode=True)
    if request.method == "POST":
        guestname = request.form.get('name')
        comment = request.form.get('comment')
        if current_user.is_authenticated:
            if not comment:
                flash('comment section cannot be empty', category='error')
                return redirect(url_for('views.view_post',id=id,slug=slug_))
        else:
            if not guestname :
                flash('name section cannot be empty', category='error')
                return redirect(url_for('views.view_post',id=id,slug=slug_))
            if not comment:
                flash('comment section cannot be empty', category='error')
                return redirect(url_for('views.view_post',id=id,slug=slug_))
            
        if current_user.is_authenticated:
            post = Comment(guestname =current_user.username, Comment=comment, post_id=id)                
        else:
            post = Comment(guestname =guestname, Comment=comment, post_id=id)
        db.session.add(post)
        db.session.commit()
        flash(f'{post.guestname} commented!', category='success')
        return redirect(url_for('views.view_post',id=id,slug=slug_))
        
    return render_template('view_post.html',post_view=post_view)


@views.route("/category", methods=['GET','POST'])
@login_required
def add_category():
    if request.method == "POST":
        cat = request.form.get('category')
        if not cat :
            flash('Input items cannot be empty', category='error')
        else:
            category_exist = Category.query.filter_by(category = cat).first()
            if category_exist:
                flash("category added..")
                return redirect(url_for('views.create_post'))
        category = Category(category = cat,cat_user =current_user.id)
        db.session.add(category)    
        db.session.commit()
        flash("category added..")
        return redirect(url_for('views.create_post'))
    return render_template('posts.html')

    

@views.route("/category_del/<int:id>/", methods=['GET','POST'])
@login_required
def del_category(id):
    cat =  Category.query.filter_by(id=id).first()
    if request.method == "POST":
        if not cat :
            flash('Input items cannot be empty', category='error')
        else:
            if current_user.id == cat.cat_user:
                db.session.delete(cat)
                db.session.commit()
                flash("category deleted...")
            else:
                flash('not worked', category='error')
            return redirect(url_for('views.home'))
    return render_template('home.html')


@views.route("/likepost/<post_id>", methods=['POST'])
@login_required
def like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    
    
    if not post:
        return jsonify({'error': 'Post does not exist.'}, 400)
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(user_id=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
        

    return jsonify({"likes": len(post.likes),"liked": current_user.id in map(lambda x: x.user_id, post.likes)})



@views.route("/dashboard")
@login_required
def user_dashboard():
    return render_template("dashboard.html")


@views.route("/pic", methods=['POST'])
@login_required
def picture ():
    pic = request.files['image1']
    if not pic:
        flash('No file')
        return redirect(url_for('views.home')),400
    else:
        filename = secure_filename(pic.filename)
        if pic.filename =="":
            flash('No selected file')
            return redirect(url_for('views.home'))
        else:    
            type=pic.mimetype
            img=Image(img=pic.read(),type=type,img_name=filename ,user_id=current_user.id)
            db.session.add(img)
            db.session.commit()
        return redirect(url_for('views.home'))
    

@views.route("pic/<int:id>/", methods=['GET', 'POST'])
def view_img(id):
    img_view = Image.query.filter_by(id=id).first() 
    if not img_view:
        flash ('image not found',category='error')
        return redirect(url_for('views.home'))
    else:
        if img_view.type ==" ":
            flash('its not a image')
        else:
            return Response(img_view.img,mimetype=img_view.type)
    return render_template("dashboard.html",current_user=current_user, img_view=img_view)
