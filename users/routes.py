import os.path
import secrets
from PIL import Image

from flask import Blueprint, render_template, flash, url_for, request, abort, \
  current_app
from flask_login import login_required, logout_user, login_user, current_user

from core import login_manager
from werkzeug.utils import redirect

from core import db
from users.Utils import encrypt, validate_encrypted
from users.forms import LoginForm, SignUpForm, ProfileForm, UserEmailForm
from users.models import User

users = Blueprint('users', __name__, template_folder='templates',
                  static_folder='static')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('users.login'))

@users.route("/login/", methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    print(user)
    if user and validate_encrypted(form.password.data, user.password):
      login_user(user)
      flash('Logged in successfully', 'success')
      return redirect(request.args.get('next') or url_for('blogs.home'))
    else:
      flash('Invalid Email or password, please provide validate credentials!', 'danger')
  return render_template('users/login.html', form=form)

@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))


@users.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
  form = SignUpForm()
  if form.validate_on_submit():
    flash('Successful Signup. Please Log In!', 'success')
    user = User(first_name=form.first_name.data, last_name=form.last_name.data,
                email=form.email.data,
                password=encrypt(form.password.data))
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('users.login'))
  return render_template('users/sign-up.html', form=form)


def save_profile_image(profile_image):
  random_hex = secrets.token_hex(8)
  _, file_ext = os.path.splitext(profile_image.filename)
  file_name = random_hex+file_ext
  file_path = os.path.join(current_app.root_path, 'static/profile_pics', file_name)
  small_image = Image.open(profile_image)
  small_image.thumbnail((100, 100))
  small_image.save(file_path)
  return file_name


@users.route("/profile", methods=['GET', 'POST'])
def profile():
  form = ProfileForm(first_name=current_user.first_name, last_name=current_user.last_name, profile_image = current_user.profile_image)
  print('form submitted...........')
  if form.validate_on_submit():
    print(form.profile_image.data)
    flash('Profile updated successfully!', 'success')
    current_user.first_name=form.first_name.data
    current_user.last_name=form.last_name.data

    if form.profile_image.data:
      current_user.profile_image = save_profile_image(form.profile_image.data)
    db.session.commit()
    return redirect(url_for('users.profile'))
  else:
    print(form.errors)
  return render_template('users/profile.html', form=form)

@users.route("/forgot_password")
def forgot_password():
  form = UserEmailForm()


