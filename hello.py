#!usr/bin/env python3
#coding = utf-8
from flask import  Flask, render_template, redirect, url_for, session, flash
from flask_script import Manager,Shell
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
import os

basedir = os.path.abspath(os.path.dirname(__file__))
#os.path.abspath(path)返回path规范化的绝对路径
#os.path.dirname(path)返回path最后的文件名

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
#数据库配置
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

class NameFrom(Form):
    name = StringField('What is youe name ?', validators = [Required()])
    submit = SubmitField('Submit')



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

