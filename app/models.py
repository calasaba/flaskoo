#数据库模型
from . import db
from . import login_manger
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
#generate_password(password, method=pbkdf2:sha1, salt_length=8)
#这个函数讲原始密码作为参数输入，以字符串形式输出密码散列值，输出的值可保存在用户数据库中

#check_password_hash(hash, password) 这个函数的参数从数据库中取出密码散列值和用户输入的密码，返回True表明密码正确



#定义模型，模型一般是一个Python类，类是相当于数据库中的表，类中的属性对应数据库表中的列
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

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


    def __repr__(self):
        return '<User %r>' % self.username
 #加载用户的回调函数  使用指定的标识符加载用户  如果能找到用户，这个函数必须返回用户对象，否则应该返回None
@login_manger.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))