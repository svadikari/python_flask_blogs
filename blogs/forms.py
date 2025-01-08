from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.fields.simple import SubmitField, HiddenField
from wtforms.validators import DataRequired, length


class BlogForm(FlaskForm):
  id = HiddenField()
  title = StringField(validators=[DataRequired(), length(min=5, max=50)])
  details = TextAreaField(validators=[DataRequired(), length(max=2000)])
  submit = SubmitField('Post')
