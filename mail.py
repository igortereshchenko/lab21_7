import hashlib

from flask import *
from sqlalchemy.exc import DatabaseError

from flask_app import *

from dao.db import *
from dao.orm.model import *
from forms.mail_form import *

from datetime import datetime
from plotly.utils import PlotlyJSONEncoder
import json
import plotly.graph_objs as go


@app.route('/plotly', methods=['GET'])
def plotly():
    db = PostgresDb()

    x = []
    y = []

    mail_dict = {}

    mails = db.sqlalchemy_session.query(Mail).all()

    for mail in mails:
        if mail.mail_datetime in mail_dict:
            mail_dict[mail.mail_datetime] += 1
        else:
            mail_dict[mail.mail_datetime] = 1

    for (date, count) in mail_dict.items():
        x.append(date)
        y.append(count)

    scatter = go.Scatter(
        x=x,
        y=y,
    )

    data = [scatter]

    ids = [1]
    names = ["Datetime count"]
    graph_json = json.dumps(data, cls=PlotlyJSONEncoder)
    return render_template('plotly.html', graphJSON=graph_json, ids=ids, names=names)

@app.route('/show', methods=['GET'])
def mail():
    db = PostgresDb()

    result = db.sqlalchemy_session.query(Mail).all()
    return render_template('show.html', mails=result)


@app.route('/insert', methods=['GET', 'POST'])
def new_mail():
    form = MailForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('mail_form.html', form=form, form_name="New mail", action="insert",
                                   method='POST')
        else:
            mail = Mail(
                mail_id=form.mail_id.data,
                mail_domain=form.mail_domain.data,
                mail_receiver=form.mail_receiver.data,
                mail_sender=form.mail_sender.data,
                mail_datetime=form.mail_datetime.data
            )

            db = PostgresDb()
            db.sqlalchemy_session.add(mail)
            try:
                db.sqlalchemy_session.commit()
            except DatabaseError as e:
                db.sqlalchemy_session.rollback()
                print(e)
                return redirect('/show')

            return redirect('/show')

    return render_template('mail_form.html', form=form, form_name="New mail", action="insert")


@app.route('/edit_soft', methods=['GET', 'POST'])
def edit_soft():
    form = UsersForm()

    if request.method == 'GET':

        user_id = request.args.get('user_id')
        db = PostgresDb()
        user = db.sqlalchemy_session.query(Users).filter(Users.user_id == user_id).one()

        form.username.data = user.username
        form.email.data = user.email
        form.password.data = ''

        return render_template('users_form.html', form=form, form_name="Edit user",
                               action="edit_user?user_id=" + request.args.get('user_id'))
    else:
        if not form.validate():
            return render_template('users_form.html', form=form, form_name="Edit user",
                                   action="edit_user?user_id=" + request.args.get('user_id'))
        else:
            db = PostgresDb()

            user = db.sqlalchemy_session.query(Users).filter(Users.user_id == request.args.get('user_id')).one()

            user.username = form.username.data
            user.email = form.email.data
            user.password_hash = hashlib.sha256(form.password.data.encode('utf-8')).hexdigest()

            try:
                db.sqlalchemy_session.commit()
            except DatabaseError as e:
                db.sqlalchemy_session.rollback()
                print(e)
                return redirect('/users')

            return redirect('/users')


@app.route('/delete_soft', methods=['POST'])
def delete_soft():
    user_id = request.form['user_id']

    db = PostgresDb()

    result = db.sqlalchemy_session.query(Users).filter(Users.user_id == user_id).one()

    db.sqlalchemy_session.delete(result)
    try:
        db.sqlalchemy_session.commit()
    except DatabaseError as e:
        db.sqlalchemy_session.rollback()
        print(e)
        return redirect('/users')

    return redirect('/users')


@app.route('/get', methods=['GET', 'POST'])
def add_soft():
    mail_1 = Mail(
        mail_id=1,
        mail_domain='gmail.com',
        mail_receiver='asdaqsbvv@gmail.com',
        mail_sender='q3wljrhawkjrhj@mail.ru',
        mail_datetime=datetime.now()
    )

    mail_2 = Mail(
        mail_id=2,
        mail_domain='mail.ru',
        mail_receiver='sdsdasdaqsbvv@gmail.com',
        mail_sender='q3wljrsdhawkjrhj@mail.ru',
        mail_datetime=datetime.now()
    )

    mail_3 = Mail(
        mail_id=3,
        mail_domain='gmail.com',
        mail_receiver='ad@gmail.com',
        mail_sender='ffs1@mail.ru',
        mail_datetime=datetime.now()
    )

    db = PostgresDb()
    db.sqlalchemy_session.add(mail_1)
    db.sqlalchemy_session.add(mail_2)
    db.sqlalchemy_session.add(mail_3)

    try:
        db.sqlalchemy_session.commit()
    except DatabaseError as e:
        db.sqlalchemy_session.rollback()
        print(e)

    return render_template('index.html')
