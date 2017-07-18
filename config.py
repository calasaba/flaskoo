#程序的配置
import os
#数据库配置
basedir = os.path.abspath(os.path.dirname(__file__))
#os.path.abspath(path)返回path规范化的绝对路径
#os.path.dirname(path)返回path最后的文件名
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or 'hard to guess string'

    # SQLALCHEMY_COMMIT_ON_TRERDOWN键，设置为True，每次请求结束后会自动提交数据库中的变动
    SQLALCHEMY_COMMIT_ON_TRERDOWN = True
    # 如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它。
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #email设置，email目前不能用
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin < 853141976 @ qq.com > '
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    #执行对当前配置环境的初始化
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    #邮箱设置，邮箱目前不能用
    DEBUG = True
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 465
    # app.config['MAIL_USE_TLS'] = True
    MAIL_USE_SSL = True
    # app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    MAIL_USERNAME = "calasaba123@163.com"
    # app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    MAIL_PASSWORD = "jie111cwj"
    # app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
    # app.config['FLASKY_ADMIN'] = "853141976@qq.com"
    '''
    app.config['MAIL_SERVER'] = 'smtp.qq.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_TLS'] = True
    #app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    #app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_USERNAME'] = "853141976@qq.com"
    app.config['MAIL_PASSWORD'] = "icrzguuprjmmbedh"
    '''
    # 程序使用的URL必须保存到Flask配置对象的SQLALCHEMY_DATABASE_URI键中
    #配置开发环境的数据库地址
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
class TestingConfig(Config):
    TESTING = True
    # 程序使用的URL必须保存到Flask配置对象的SQLALCHEMY_DATABASE_URI键中
    # 配置开发环境的数据库地址
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

class ProductionConfig(Config):
    #配置生产环境的数据库地址
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or\
                              'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
    'development' : DevelopmentConfig ,
    "testing" : TestingConfig ,
    "production" : ProductionConfig ,
    "default" : DevelopmentConfig

}



