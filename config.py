import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'hard to guess string' or os.environ.get('SECRET_KEY')
    SQLALCHEMY_COMMIT_ON_TRERDOWN = True
    # SQLALCHEMY_COMMIT_ON_TRERDOWN键，设置为True，每次请求结束后会自动提交数据库中的变动
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它。

    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <853141976@qq.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = True
    # app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    # app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    MAIL_USERNAME = "853141976@qq.com"
    MAIL_PASSWORD = "icrzguuprjmmbedh"

    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir,'data.sqlite')

config = {
    'development':DevelopmentConfig,
    'testing': TestConfig,
    'production':ProductionConfig,
    'default':DevelopmentConfig
}
