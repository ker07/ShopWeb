from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from datetime import datetime
from time import time
import jwt


app = Flask(__name__)
app.config['SECRET_KEY'] = "asdf;nao9weufr;weu21389y;wf"
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///shopwebapp.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

worker_list = [1]

#CONFIGURE TABLE IN DATABASE
class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(50))
    sex = db.Column(db.String(10))
    birthday = db.Column(db.Date)
    cart_item = relationship("CartItem", back_populates="buyer")
    bought_item = relationship("SoldItem", back_populates="buyer")
    comment = relationship("Comment", back_populates="comment_author")
    created_date = db.Column(db.DateTime, default=datetime.now)
    updated_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            _id = jwt.decode(token, app.config['SECRET_KEY'],
                             algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

class Item(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(10), nullable=False)
    size = db.Column(db.String(10), nullable=False)
    color = db.Column(db.String(10), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.now)
    updated_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    start_selling_time = db.Column(db.DateTime)
    stop_selling_time = db.Column(db.DateTime)


class CartItem(db.Model):
    __tablename__ = "cartitems"
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    quantity = db.Column(db.Integer, nullable=False)
    buyer = relationship("User", back_populates="cart_item")
    buyer_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_date = db.Column(db.DateTime, default=datetime.now)
    updated_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class SoldItem(db.Model):
    __tablename__ = "solditems"
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    quantity = db.Column(db.Integer, nullable=False)
    buyer = relationship("User", back_populates="bought_item")
    buyer_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_date = db.Column(db.DateTime, default=datetime.now)
    updated_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    comment_author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comment_author = relationship("User", back_populates="comment")
    created_date = db.Column(db.DateTime, default=datetime.now)
    updated_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class Picture(db.Model):
    __tablename__ = "pictures"
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    created_date = db.Column(db.DateTime, default=datetime.now)
    updated_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
