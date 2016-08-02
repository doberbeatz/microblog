from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length


class LoginForm(Form):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class RegisterForm(Form):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[
        DataRequired(),
        Length(min=6, max=120),
        EqualTo('password_confirm', message='Password must match')
    ])
    password_confirm = PasswordField('password_confirm')


class EditForm(Form):
    username = StringField('username', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])


class PostForm(Form):
    post = TextAreaField('post', validators=[DataRequired()])
