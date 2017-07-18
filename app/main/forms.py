#表单对象
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class NameFrom(FlaskForm):
    name = StringField('What is youe name ?', validators = [Required()])
    submit = SubmitField('Submit')