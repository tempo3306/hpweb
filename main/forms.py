from flask_wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField,StringField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from ..models import Role, User ,Auction
from wtforms import StringField, PasswordField, BooleanField, SubmitField,FieldList,FileField,SelectField

class NameForm(Form):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class BID_dataForm(Form):
#  IDnumber = SelectField("设备类型", choices=[('手持机', '手持机'), ('脚扣', '脚扣')])
    description= StringField("标书说明",validators=[DataRequired()])
    IDnumber = StringField("身份证号", validators=[DataRequired(),Length(18),Regexp('^[0-9](X|x){0,1}',message=u'请输入正确的身份证号')])
    BIDnumber = StringField("标书号", validators=[DataRequired(),Length(8),Regexp('^[0-9]',message=u'请输入正确的标书号')])
    BIDpassword = StringField("标书密码", validators=[DataRequired(),Length(4),Regexp('^[0-9]',message=u'请输入正确的标书密码')])
# 提交按钮
    submit = SubmitField('创建标书号')

class BID_actionForm(Form):
    diff_choices=[(i*100+400,i*100+400) for i in range(12)]
    refer_time_choices=[(i*0.1+40,"%.1f"%(i*0.1+40)) for i in range(151)]
    bid_time_choices=[(i*0.1+40,"%.1f"%(i*0.1+40)) for i in range(151)]
    delay_time_choices=[(i*0.1,"0.%d"%i) for i in range(10)]
    ahead_price_choices=[(i*100,i*100) for i in range(4)]
    date_month=[("2017年%d月"%i,"2017年%d月"%i)  for i in range(8,13)]
    date_month2=[("2018年%d月"%i,"2018年%d月"%i) for i in range(1,13)]
    date_month.extend(date_month2)

    refer_time = SelectField(u"加价时间",coerce=float,choices=refer_time_choices,default=(50,50)) #参考时间
    diff = SelectField(u"相差价格",coerce=int, choices=diff_choices) #参考时间差价
    bid_time = SelectField(u"强制出价时间",coerce=float,choices=bid_time_choices,default=(55,55)) #出价截止时间
    delay_time = SelectField(u"出价延迟",coerce=float, choices=delay_time_choices) #出价延迟时间，0.1~0.9
    ahead_price = SelectField(u"出价提前",coerce=int,choices=ahead_price_choices,default=(100,100)) #出价提前价格
    date= SelectField(u"拍牌月份",coerce=str,choices=date_month,default=date_month[0])
    auction_use=SelectField("标书选择",coerce=int)
    action_user = SelectField('拍手选择：', coerce=int)
# 提交按钮
    submit = SubmitField('创建策略')
    def __init__(self, user, *args, **kwargs):
        super(BID_actionForm, self).__init__(*args, **kwargs)
        self.action_user.choices = [(user.id, user.username)
                             for user in User.query.order_by(User.username).all()]
        self.auction_use.choices=[(auction.id,auction.description)
                    for auction in Auction.query.order_by(Auction.description).all()]


        self.user = user



class Edit_BID_dataForm(Form):
    description = StringField("标书说明", validators=[DataRequired()])
    IDnumber = StringField("身份证号", validators=[DataRequired(),Length(18),Regexp('^[0-9](X|x){0,1}',message=u'请输入正确的身份证号')])
    BIDnumber = StringField("标书号", validators=[DataRequired(),Length(8),Regexp('^[0-9]',message=u'请输入正确的标书号')])
    BIDpassword = StringField("标书密码", validators=[DataRequired(),Length(4),Regexp('^[0-9]',message=u'请输入正确的标书密码')])


# 提交按钮
    submit = SubmitField('提交修改')
    delete = SubmitField('删除')


class Edit_BID_actionForm(Form):
    diff_choices=[(i*100+400,i*100+400) for i in range(12)]
    refer_time_choices=[(i*0.1+40,"%.1f"%(i*0.1+40)) for i in range(151)]
    bid_time_choices=[(i*0.1+40,"%.1f"%(i*0.1+40)) for i in range(151)]
    delay_time_choices=[(i*0.1,"0.%d"%i) for i in range(10)]
    ahead_price_choices=[(i*100,i*100) for i in range(4)]
    date_month=[("2017年%d月"%i,"2017年%d月"%i)  for i in range(8,13)]
    date_month2=[("2018年%d月"%i,"2018年%d月"%i) for i in range(1,13)]
    date_month.extend(date_month2)

    refer_time = SelectField(u"加价时间",coerce=float,choices=refer_time_choices,default=(50,50)) #参考时间
    diff = SelectField(u"相差价格",coerce=int, choices=diff_choices) #参考时间差价
    bid_time = SelectField(u"强制出价时间",coerce=float,choices=bid_time_choices,default=(55,55)) #出价截止时间
    delay_time = SelectField(u"出价延迟",coerce=float, choices=delay_time_choices) #出价延迟时间，0.1~0.9
    ahead_price = SelectField(u"出价提前",coerce=int,choices=ahead_price_choices,default=(100,100)) #出价提前价格
    date= SelectField(u"拍牌月份",coerce=str,choices=date_month,default=date_month[0])
    auction_use=SelectField("标书选择",coerce=int)
    action_user = SelectField('拍手选择：', coerce=int)
    # 提交按钮
    submit = SubmitField(u'提交修改')
    delete = SubmitField(u'删除策略')

# 提交按钮
    submit = SubmitField(u'提交修改')
    delete = SubmitField(u'删除策略')

    def __init__(self, user, *args, **kwargs):
        super(Edit_BID_actionForm, self).__init__(*args, **kwargs)
        self.action_user.choices = [(user.id, user.username)
                                    for user in User.query.order_by(User.username).all()]
        self.auction_use.choices=[(auction.id,auction.description)
                                  for auction in Auction.query.order_by(Auction.description).all()]


        self.user = user

###文件上传
class FileForm(Form):
    file1=FileField('第一次出价')
    file2=FileField('最后一次出价')
    file3=FileField('结果')
    file4=FileField('出价视频')
    submit=SubmitField('Submit')

###查询
class InquiryForm(Form):
    keyword=StringField('内容')
    submit=SubmitField('查询')





#------------------------------------------停用




class EditProfileForm(Form):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')


class EditProfileAdminForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')




class CommentForm(Form):
    body = StringField('Enter your comment', validators=[DataRequired()])
    submit = SubmitField('Submit')


####修改过
class BulletinForm(Form):
    dt=StringField('时间')
    price=StringField('价格',validators=[DataRequired()])
    names = FieldList(StringField('名称'), label='物品列表', min_entries=1)


