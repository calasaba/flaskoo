#!usr/bin/env python3
#coding = utf-8
from flask import  Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello world!</h1>\n<h2>你好啊，世界。</h2>'

if __name__ == '__main__':
    app.run()

