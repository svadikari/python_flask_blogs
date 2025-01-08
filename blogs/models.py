from datetime import datetime

from core import db

class Blog(db.Model):
  id = db.Column(db.Integer, unique=True, primary_key=True)
  title = db.Column(db.String(200), nullable=False)
  details = db.Column(db.String(), nullable=False)
  created = db.Column(db.DateTime, nullable=False, default=datetime.now)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

  def __repr__(self):
    return f'Blog (title={self.title})'