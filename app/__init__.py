#工厂函数，延迟创建程序实例，把创建过程移到可显式调用的工厂函数中

from flask import  Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager

login_manger = LoginManager()
login_manger.session_protection = "strong"#设置安全等级，防止用户对话遭篡改
login_manger.login_view = "auth.login"#设置登录页面的端点

db = SQLAlchemy()
bootstrap = Bootstrap()
moment = Moment()
mail = Mail()
#creat_app 程序的工厂函数，接受一个参数，参数就是程序使用的配置名
def create_app(config_name):
    app = Flask(__name__)
    #from_object方法，导入保存的配置
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    #初始化扩展
    bootstrap.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    login_manger.init_app(app)
    #附加路由和自定义的错误页面 main蓝本
    from .main import  main  as main_blueprint
    app.register_blueprint(main_blueprint)
    #auth 蓝本
    from .auth import  auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    #url_prefix 使用了这个参数，注册后蓝本中定义的所有路由都会加上指定的前缀
    #返回创建的程序示例
    return  app