from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model,UserMixin):
    """User account model."""
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    posts = db.relationship('Post', back_populates ='user')
    likes = db.relationship('Like', back_populates ='user', passive_deletes=True)
    image_ = db.relationship('Image', back_populates='image_', passive_deletes=True)


class Category(db.Model):
    """Users category model"""
    __tablename__ = "category"
    id = db.Column(db.Integer,primary_key = True)
    cat_user = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(100))
    posts = db.relationship('Post',back_populates='category')
    
class Post(db.Model):
    """Users posts model."""
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id',ondelete="CASCADE"), nullable=False)
    user = db.relationship('User', back_populates ='posts')
    comments = db.relationship('Comment', back_populates ='post', passive_deletes=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category',back_populates='posts')
    likes = db.relationship('Like', back_populates='posts', passive_deletes=True)
    
class Comment(db.Model):
    """Users comment model"""
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    guestname = db.Column(db.String(150))
    Comment = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=func.now())
    post_id = db.Column(db.Integer, db.ForeignKey('post.id',ondelete="CASCADE"), nullable=False)
    post = db.relationship('Post', back_populates ='comments', passive_deletes=True)
    
    
class Like(db.Model):
    """Users like model"""
    __tablename__ = "like"
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id', ondelete="CASCADE"), nullable=False)
    user = db.relationship('User', back_populates='likes', passive_deletes=True)
    posts = db.relationship('Post', back_populates='likes', passive_deletes=True)
    
class Image(db.Model):
    """Users image model"""
    __tablename__ = "image"
    id = db.Column(db.Integer, primary_key=True)
    img=db.Column(db.LargeBinary,unique=False,nullable=False)
    img_name=db.Column(db.Text,nullable=False)
    type=db.Column(db.Text,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    image_ = db.relationship('User', back_populates='image_', passive_deletes=True)
