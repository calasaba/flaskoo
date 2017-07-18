#工厂函数，延迟创建程序实例，把创建过程移到可显式调用的工厂函数中

from flask import  Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from config import config

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
    #附加路由和自定义的错误页面
    from .main import  main  as main_blueprint
    app.register_blueprint(main_blueprint)
    #返回创建的程序示例
    return  app