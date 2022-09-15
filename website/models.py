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
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    posts = db.relationship("Post", back_populates = "name")


class Post(db.Model,UserMixin):
    """Post model"""
    __tablename__ = "post"
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(150))
    category = db.Column(db.String(150))
    content = db.Column(db.String)
    publish_time = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable= False)
    name = db.relationship("User", back_populates = "posts")

