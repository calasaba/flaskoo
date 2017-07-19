from flask_wtf import  Form
from wtforms import SubmitField, StringField, PasswordField, BooleanField
from wtforms.validators import Required, Length, Email

class LoginForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField("Password", validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    sumbit = SubmitField('Log In')