from ext import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class NewProduct(db.Model):
    __tablename__ = "newproducts"

    id = db.Column(db.Integer(), primary_key=True )
    name = db.Column(db.String())
    price = db.Column(db.Integer())
    image_path = db.Column(db.String())
    description = db.Column(db.String())
    country = db.Column(db.String())
    address = db.Column(db.String())
    author = db.Column(db.String())
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String())
    gender = db.Column(db.String())
    path = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())
    birthday = db.Column(db.Date())
    role = db.Column(db.String())

    def __init__(self, path, username, birthday, password, gender, email, role="Guest"):
        self.path = path
        self.username = username
        self.gender = gender
        self.email = email
        self.birthday = birthday
        self.password = generate_password_hash(password)
        self.role = role



    def check_password(self, password):
        return check_password_hash(self.password, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class Rating(db.Model):
    __tablename__ = "ratings"

    id = db.Column(db.Integer(), primary_key=True)
    product_id = db.Column(db.Integer(), nullable=False)
    rating = db.Column(db.Integer, nullable=False)



class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer(), primary_key=True)
    product_id = db.Column(db.Integer(), nullable=False)
    comment = db.Column(db.Integer, nullable=False)
    author = db.Column(db.String())
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Like(db.Model):
    __tablename__ = "likes"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('newproducts.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Dislike(db.Model):
    __tablename__ = "dislikes"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('newproducts.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))