from flask_wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField, \
    SubmitField, StringField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from ..models import Role, User
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FieldList, FileField


class PostForm(Form):
    title = TextAreaField(r"输入标题", validators=[DataRequired()])
    body = TextAreaField(r"输入文章内容", validators=[DataRequired()])
    submit = SubmitField('Submit')

#编辑表单
class Bid_articleForm(Form):
    body = TextAreaField("编辑文章?", validators=[DataRequired(u"内容不能为空")]) #生成markdown预览
    submit = SubmitField('提交')