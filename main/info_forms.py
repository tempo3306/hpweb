from flask_wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField, \
    SubmitField, StringField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from ..models import Role, User
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FieldList, FileField


class PostForm(Form):
    title = TextAreaField(r"输入标题", validators=[Required()])
    body = TextAreaField(r"输入文章内容", validators=[Required()])
    submit = SubmitField('Submit')
