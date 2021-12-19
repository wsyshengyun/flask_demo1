from flask_mail import Message 
from app import mail ,app
from threading import Thread
from flask import render_template

def send_email(subject, sender, recipients, text_body, html_body):
    """[summary]
    Args:
        subject : 邮箱的标题
        sender : 发件人
        recipients : 收件人列表
        text_body : 内容
        html_body : 内容
    
    """    
    msg = Message(subject=subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[Microblog] Reset Your Password'
        ,sender=app.config['MAIL_DEFAULT_SENDER']
        ,recipients=[user.email]  # recipient接受者
        ,text_body=render_template('email/reset_password.txt',user=user, token=token)
        ,html_body=render_template('email/reset_password.html', user=user, token=token)
        )