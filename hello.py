#!usr/bin/env python3
#coding = utf-8
import os
from flask_script import Manager,Shell
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db
from app.models import User, Role

app = create_app(os.getenv("FLASK_CONFIG") or 'default')

manager = Manager(app)
migrate = Migrate(app, db)


#集成python shell
def make_shall_content():
    return dict(app = app, db = db, User = User, Role = Role)
manager.add_command('Shell', Shell(make_context = make_shall_content))
manager.add_command('db',MigrateCommand)

'''
@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name = name)
'''
@manager.command
def test():
    """
    Run the unit tests.
    """
    import  unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':

    manager.run()

