#在app包中创建一个子包main，用于保存蓝本
from flask import Blueprint
main = Blueprint('main', __name__)
#蓝本的构造函数有两个必须指定的参数：蓝本的名字 和  蓝本所在的包或模块
from . import views, errors

#程序的路由保存在app/main/views.py 模块中
#程序的错误处理程序保存在app/main/errors.py 模块中#导入 这两个模块就能把路由和错误处理程序与蓝本关联起来
