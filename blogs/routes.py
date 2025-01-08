from flask import Blueprint, render_template, url_for, flash, request
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from core import db

from blogs.forms import BlogForm
from blogs.models import Blog

blogs = Blueprint('blogs', __name__, template_folder='templates',
    static_folder='static')

@blogs.route("/")
@login_required
def home():
  page = request.args.get('page', 1, type=int)
  per_page = request.args.get('per_page', 3, type=int)
  pagination = Blog.query.order_by(Blog.created.desc()).paginate(page=page, per_page=per_page)

  return render_template('blogs/home.html', pagination=pagination, per_page=per_page)

@blogs.route('/blog', methods=['GET', 'POST'])
@login_required
def blog():
  form = BlogForm()
  if form.validate_on_submit():
    if form.id.data:
      blog = Blog.query.get_or_404(form.id.data)
      blog.title=form.title.data
      blog.details = form.details.data
    else:
      blog = Blog(title=form.title.data, details=form.details.data, author=current_user)
    db.session.add(blog)
    db.session.commit()
    flash('Post has been created successfully!', 'success')
    return redirect(url_for('blogs.home'))
  return render_template('blogs/blog.html', form=form)

@blogs.route('/blog/<int:id>', methods=['GET'])
@login_required
def update_blog(id):
  blog_record = Blog.query.get_or_404(id)
  form = BlogForm(id=blog_record.id, title=blog_record.title, details=blog_record.details)
  return render_template('blogs/blog.html', form=form)

@blogs.route('/blogs/<int:id>/delete', methods=['POST'])
@login_required
def delete_blog(id):
  blog_record = Blog.query.get_or_404(id)
  db.session.delete(blog_record)
  db.session.commit()
  return redirect(url_for('blogs.home'))
