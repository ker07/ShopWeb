from flask_mail import Message
from flask import render_template
from model import app
from threading import Thread
from flask_mail import Mail

mail = Mail(app)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_password_reset_mail(user):
    token = user.get_reset_password_token()
    send_email(
        '[Shoppp] Reset Your Password',
        recipients=[user.email],
        text_body=render_template('reset_password_mail.txt', user=user, token=token),
        html_body=render_template('reset_password_mail.html', user=user, token=token)
    )