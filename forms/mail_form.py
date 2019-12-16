from flask_wtf import Form
from wtforms import ValidationError, IntegerField, StringField, validators, DateField, SubmitField
from dao.db import *
from dao.orm.model import *
from datetime import datetime


def validate_date(form, field):
    if field.data <= datetime.now().date():
        raise ValidationError('Datetime > now')

class MailForm(Form):
    mail_id = IntegerField("ID: ", [
        validators.DataRequired("Enter ID.")
    ])

    mail_domain = StringField("Domain: ", [
        validators.DataRequired("Enter domain."),
        validators.any_of(['gmail.com', 'kpi.ua'])
    ])

    mail_receiver = StringField("Receiver: ", [
        validators.DataRequired("Enter receiver"),
    ])

    mail_sender = StringField("Sender: ", [
        validators.DataRequired("Enter sender"),
    ])

    mail_datetime = DateField("Date: ", [
        validators.DataRequired("Enter date"),
        validate_date
    ])

    submit = SubmitField("Save")