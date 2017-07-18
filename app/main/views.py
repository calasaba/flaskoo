#蓝本中定义的程序路由

from datetime import datetime
from flask import render_template, session ,redirect ,url_for

from . import main
from .forms import NameFrom
from .. import db
from ..models import User

@main.route('/', methods = ['GET', 'POST'])
def index():
    form = NameFrom()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.name.data).first()
        if user is None:
            user = User(username = form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False

            if True:

                '''
                msg = Message('New User is coming!', sender="calasaba123@163.com",
                              recipients=["853141976@qq.com"])
                msg.body = "快出来，接客了"
                with app.app_context():
                    mail.send(msg)
                '''
                #send_email(app.config['FLASKY_ADMIN'], 'New User',
                           #'mail/new_user', user = user)


        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('.index'))
    return render_template('index.html',
                           current_time = datetime.utcnow(),
                           form = form,
                           name = session.get('name'),
                           known = session.get('known', False))