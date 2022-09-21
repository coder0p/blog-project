from flask import Flask, render_template,request,flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from sqlalchemy.sql import func
from flask_login import UserMixin


app = Flask(__name__)
app.config['SECRET_KEY'] = "helloworld"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


    
    
class User(db.Model,UserMixin):
    """User account model."""
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    posts = db.relationship('Post', back_populates ='user')


class Post(db.Model):
    """Users posts model."""
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    category = db.Column(db.String(150))
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates ='posts')
    comments = db.relationship('Comment', back_populates ='post')

    
class Comment(db.Model):
    """Users comment model"""
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    guestname = db.Column(db.String(150))
    Comment = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=func.now())
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', back_populates ='comments')

    
@app.route("/", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        if email_exists:
            flash('Email is already in use.', category='error')
        elif username_exists:
            flash('Username is already in use.', category='error')
            

        else:
            
            new_user = User(email=email, username=username, 
                            password=generate_password_hash(
                                password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('User created!')

    return render_template("registration.html")


if __name__ == "__main__":
    db.create_all()
    print('Creating database is success...')
   # app.run(debug=True)