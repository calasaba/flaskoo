#数据库模型
from . import db
from . import login_manger
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

#generate_password(password, method=pbkdf2:sha1, salt_length=8)
#这个函数讲原始密码作为参数输入，以字符串形式输出密码散列值，输出的值可保存在用户数据库中

#check_password_hash(hash, password) 这个函数的参数从数据库中取出密码散列值和用户输入的密码，返回True表明密码正确



#定义模型，模型一般是一个Python类，类是相当于数据库中的表，类中的属性对应数据库表中的列
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')
    #用户权限
    default = db.Column(db.Boolean, default = False, index = True)
    permissions = db.Column(db.Integer)

    @staticmethod
    def insert_roles():
        roles = {
            "Users" : (Permission.FOLLOW |
                       Permission.COMMENT |
                       Permission.WRITE_ARTICLES , True),
            "Moderator" : (Permission.FOLLOW |
                           Permission.COMMENT |
                           Permission.WRITE_ARTICLES |
                           Permission.MODERATE_COMMITS, False),
            "Administrator" : (0xff,False)
        }
        for r in roles:
            role = Role.query.filter_by(name = r).first()
            if role is None:
                role = Role(name = r)
            role.premissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()


    def __repr__(self):
        return '<Role %r>' % self.name
class Permission:
    FOLLOW = 0X01
    COMMENT = 0X02
    WRITE_ARTICLES = 0X04
    MODERATE_COMMITS = 0X08
    ADMINISTER = 0X80
    #UserMixin类 默认实现flask-login要求必须实现的 四个 方法
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    email = db.Column(db.String(64), unique = True, index = True)
    password_hash = db.Column(db.String(128))
    #@property 把一个getter方法变成属性，只读属性
    @property
    def password(self):
        raise AttributeError('password is not readable attribute')
    #只写属性，不能读取
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    #确认账户
    confirmed = db.Column(db.Boolean, default = False)
    #生成一个令牌，默认有效时间为一个小时
    def generate_confirmation_token(self, expiration = 3600):
        s = Serializer(current_app.config["SECRET_KEY"], expiration)
        return s.dumps({'confirm' : self.id})
        #dumps为指定的数据生成一个加密签名，然后对数据和签名进行序列化，生成令牌字符串
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
            #loads方法解码令牌，唯一参数是令牌字符串
        except:
            return False
        if data.get('confirm') != self.id:
            return  False
        self.confirmed = True
        db.session.add(self)
        return True
    def __repr__(self):
        return '<User %r>' % self.username
    #赋予用户角色
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKOO_ADMIN']:
                self.role = Role.query.filter_by(permissions = 0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default = True).first()
    def can(self, permissions):
        return self.role is not None and\
               (self.role.permissions and permissions) == permissions
    def is_administrator(self):
        return self.can(Permission.ADMINISTER)
class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return  False
    def is_administrator(self):
        return  False
login_manger.anonymous_user = AnonymousUser


 #加载用户的回调函数  使用指定的标识符加载用户  如果能找到用户，这个函数必须返回用户对象，否则应该返回None
@login_manger.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))