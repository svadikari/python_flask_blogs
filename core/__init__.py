from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate


class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"

def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY']= 'fldadjfasjfldsjdlsaldafskj'
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blogs.db'
  # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost:5432/blogs'
  db.init_app(app)
  migrate.init_app(app, db)
  login_manager.init_app(app)

  from blogs.routes import blogs
  from users.routes import users

  app.register_blueprint(blogs)
  app.register_blueprint(users)

  with app.app_context():
    from users.models import User
    from blogs.models import Blog
    db.create_all()

  return app
