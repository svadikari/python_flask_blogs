from email.policy import default

from flask_login import UserMixin

from core import db

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, unique=True, primary_key=True)
  first_name = db.Column(db.String(20), nullable=False)
  last_name = db.Column(db.String(20), nullable=False)
  email = db.Column(db.String(30), unique=True, nullable=False)
  password = db.Column(db.String(100), nullable=False)
  profile_image = db.Column(db.String(20), nullable=True, default='default.png')
  blogs = db.relationship('Blog', backref ='author', lazy=True)

  def __repr__(self):
    return f'User (first_name={self.first_name}, last_name={self.last_name})'