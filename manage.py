#!usr/bin/env python3
#coding=utf-8
import os
from app import creat_app, db
from app.models import  User, Role
from flask_script import  Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = creat_app(os.getenv('FLASK_CONFIG') or 'default')
manage = Manager(app)
migrate = Migrate(app, db)

#集成python shell
def make_shall_content():
    return dict(app = app, db = db, User = User, Role = Role)
manager.add_command('shell', Shell(make_context = make_shall_content))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()


