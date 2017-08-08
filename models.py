from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from markdown import markdown
import bleach
from flask import current_app, request, url_for
from flask_login import UserMixin, AnonymousUserMixin
from app.exceptions import ValidationError
from . import db, login_manager


class Permission:
    VIEW = 0x01
    SEARCH = 0x02
    EDIT = 0x04
#WRITE_ARTICLES = 0x04
#    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'Visitor':(Permission.VIEW,True),
            'Inneruser': (Permission.SEARCH|Permission.VIEW , False),
            'Manager': (Permission.SEARCH |
                          Permission.EDIT , False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name



#登录模块，用户创建
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    passwd=db.Column(db.String(32))
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)  #创建时间
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)     #最后登录时间
    avatar_hash = db.Column(db.String(32))


# 对应策略
    bids = db.relationship('Auction_data', backref='author', lazy='dynamic') #一对一  ,lazy='immediate',uselist=False
    actions = db.relationship('BID_action', backref='author', lazy='dynamic')   #一对一,uselist=False

    @property            #这可以让你将一个类方法转变成一个类属性,表示只读。
    def password(self):
        raise AttributeError('password is not a readable attribute')

    #散列密码
    @password.setter    #同时有@property和@x.setter表示可读可写,@property和@x.setter和@x.deleter表示可读可写可删除
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True


#判断是否有相应权限
    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

# 刷新用户最后登录时间
    def ping(self):
        self.last_seen = datetime.utcnow()   #UTC世界时间
        db.session.add(self)

###添加用户头像
    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or hashlib.md5(
            self.username.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

#使用编码后的用户id 字段值生成一个签名令牌
    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'id': self.id}).decode('ascii')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def __repr__(self):
        return '<User %r>' % self.username

    #####拍牌数据库
class Auction_data(db.Model):
    __tablename__ = 'bids'
    id = db.Column(db.Integer, primary_key=True)
    IDnumber = db.Column(db.Integer)
    BIDnumber = db.Column(db.Integer)
    BIDpassword = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # 对应backref
    # action_id =db.Column(db.Integer, db.ForeignKey('actions.id'))


    def __repr__(self):
        return '<Auction %r>' % self.IDnumber

    def to_json(self):
        json_post = {

            'IDnumber': self.IDnumber,
            'BIDnumber': self.BIDnumber,
            'BIDpassword': self.BIDpassword,
            'author': url_for('api.get_user', id=self.author_id,
                              _external=True),

        }
        return json_post

class BID_action(db.Model):
    __tablename__ = 'actions'
    id = db.Column(db.Integer, primary_key=True)
    diff = db.Column(db.Integer)  #参考时间差价
    refer_time = db.Column(db.Integer) #参考时间
    bid_time = db.Column(db.Integer) #出价截止时间
    delay_time = db.Column(db.Float) #出价延迟时间，0.1~0.9
    ahead_price = db.Column(db.Integer) #出价提前价格
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # auctions = db.relationship('Auction_data', backref='action', lazy='immediate') #一对一

    def __repr__(self):
        return '<BID %r>' % self.diff

#拍牌登录信息
class login_user(db.Model):
    __tablename__='Account'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String)   #用户名与User名相同
    password=db.Column(db.String)  #与Password相同，使用hash存储
    login=db.Column(db.Integer)   #登录状态
    CODE=db.Column(db.String)    #使用的标书号
    codepsd=db.Column(db.String) #标书登录密码
    ID_number=db.Column(db.Integer)
    IP=db.Column  #记录登录IP
    MAC=db.Column(db.String)     #记录登录MAC地址
    COUNT=db.Column(db.Integer)  #登录状态



#继承自Flask-Login 中的AnonymousUserMixin 类，并将其设为用户未登录时current_user 的值
#这样程序不用先检查用户是否登录，就能自由调用current_user.can() 和current_user.is_administrator()
class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

#实现一个回调函数，使用指定的标识符加载用户
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




