from .decorators import async
from flask import render_template
from flask_mail import Message
from app import app, mail
from config import ADMINS


@async
def send_async_email(main_app, msg):
    with main_app.app_context():
        mail.send(msg)


def send_mail(subject, sender, recipients, text_body, html_body):
    """ Send mail

    :type subject: str
    :type sender: str
    :type recipients: list
    :type text_body: str
    :type html_body: str
    """
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    send_async_email(app, msg)


def follower_notification(followed, follower):
    """ Email notification

    :type followed: app.models.User
    :type follower: app.models.User
    """
    send_mail('[microblog] %s is now following you!' % followed.username,
              ADMINS[0],
              [followed.email],
              render_template('follower_email.txt',
                              user=followed, follower=follower),
              render_template('follower_html.html',
                              user=followed, follower=follower))
