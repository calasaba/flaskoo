#!usr/bin/env python3
#coding = utf-8
from flask import  Flask
from flask_script import Manager

app = Flask(__name__)
manager = Manager(app)

@app.route('/')
def index():
    return '<h1>Hello world!</h1>\n<h2>你好啊，世界。</h2>'

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello %s!</h1>'%name

if __name__ == '__main__':
    manager.run()

