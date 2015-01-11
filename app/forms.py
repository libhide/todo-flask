from flask.ext.wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(Form):
  email = StringField('email', validators=[DataRequired()])
  password = PasswordField('password', validators=[DataRequired()])

class SignupForm(Form):
  name = StringField('name', validators=[DataRequired()])
  email = StringField('email', validators=[DataRequired()])
  password = PasswordField('password', validators=[DataRequired()])

class PasswordResetForm(Form):
  old_password = PasswordField('old_pass', validators=[DataRequired()])
  new_password = PasswordField('new_pass', validators=[DataRequired()])
  new_password_confirm = PasswordField('new_pass_confirm', validators=[DataRequired()])

