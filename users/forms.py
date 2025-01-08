from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileSize
from wtforms.fields.simple import EmailField, PasswordField, SubmitField, \
  StringField, FileField
from wtforms.validators import DataRequired, length, equal_to, EqualTo


class UserEmailForm(FlaskForm):
  email = EmailField(validators=[DataRequired(), length(5, 50)])
  submit = SubmitField('Sign In')

class LoginForm(UserEmailForm):
  password = PasswordField(validators=[DataRequired(), length(8, 15)])

class SignUpForm(FlaskForm):
  first_name = StringField('First Name', validators=[DataRequired(), length(1, 20)])
  last_name = StringField('Last Name', validators=[DataRequired(), length(1, 20)])
  email = EmailField('Email Address', validators=[DataRequired(), length(5,50)])
  password = PasswordField(validators=[DataRequired(), length(8, 15)])
  confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), length(8, 15), EqualTo('password', message='Password must match with confirm password')])
  submit = SubmitField('Register')


class ProfileForm(FlaskForm):
  first_name = StringField('First Name', validators=[DataRequired(), length(1, 20)])
  last_name = StringField('Last Name', validators=[DataRequired(), length(1, 20)])
  profile_image = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
  submit = SubmitField('Save')

