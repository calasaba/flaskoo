#!usr/bin/env python3
#coding = utf-8
from flask import  Flask, render_template, redirect, url_for, session, flash,current_app
from flask_script import Manager,Shell
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail, Message
from threading import Thread
import os



#os.path.abspath(path)返回path规范化的绝对路径
#os.path.dirname(path)返回path最后的文件名

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
#数据库配置
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
#程序使用的URL必须保存到Flask配置对象的SQLALCHEMY_DATABASE_URI键中
app.config['SQLALCHEMY_COMMIT_ON_TRERDOWN'] = True
#SQLALCHEMY_COMMIT_ON_TRERDOWN键，设置为True，每次请求结束后会自动提交数据库中的变动
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它。
db = SQLAlchemy(app)
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
mail = Mail(app)
#邮件配置

app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = 465
#app.config['MAIL_USE_TLS'] = True
MAIL_DEBUG = True
app.config['MAIL_USE_SSL'] = True
#app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_USERNAME'] = "calasaba123@163.com"
#app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_PASSWORD'] = "jie111cwj"
#app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
#app.config['FLASKY_ADMIN'] = "853141976@qq.com"
'''
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = True
#app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
#app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USERNAME'] = "853141976@qq.com"
app.config['MAIL_PASSWORD'] = "icrzguuprjmmbedh"
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <853141976@qq.com>'
#app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')
app.config['FLASKY_ADMIN'] = "calasaba123@163.com"
'''



#定义模型，模型一般是一个Python类，类是相当于数据库中的表，类中的属性对应数据库表中的列
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username
#数据库迁移
migrate = Migrate(app, db)
manager.add_command('db',MigrateCommand)



#集成python shell
def make_shall_content():
    return dict(app = app, db = db, User = User, Role = Role)
manager.add_command('Shell', Shell(make_context = make_shall_content))
#表单类
class NameFrom(FlaskForm):
    name = StringField('What is youe name ?', validators = [Required()])
    submit = SubmitField('Submit')
'''
#异步发送电子邮件
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
'''
@app.route('/',methods = ['GET', 'POST'])
def index():
    form = NameFrom()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.name.data).first()
        if user is None:
            user = User(username = form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False

            if True:

                '''
                msg = Message('New User is coming!', sender="calasaba123@163.com",
                              recipients=["853141976@qq.com"])
                msg.body = "快出来，接客了"
                with app.app_context():
                    mail.send(msg)
                '''
                #send_email(app.config['FLASKY_ADMIN'], 'New User',
                           #'mail/new_user', user = user)


        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html',
                           current_time = datetime.utcnow(),
                           form = form,
                           name = session.get('name'),
                           known = session.get('known', False))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name = name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
    return  render_template('500.html'),500



if __name__ == '__main__':
    db.create_all()
    manager.run()

