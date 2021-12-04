from os import truncate
from  flask import Flask 
from config import Config
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
# from models import *
from flask_login import LoginManager

from flask_avatars import Avatars

import logging
from logging.handlers import SMTPHandler
from logging.handlers import RotatingFileHandler
import os 



app = Flask(__name__)
app.config.from_object(Config) # 此app就是Flask；
app.debug=False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'

avatars = Avatars(app)

# -----------------------------------------------------------
# 添加邮件功能
# -----------------------------------------------------------
if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['mail_username'] or app.config['mail_password']:
            auth = (app.config['mail_username'], app.config['mail_password'])
        secure=None
        if app.config['mail_use_tls']:
            secure=()
        mail_handler = SMTPHandler(
            mailhost=(app.config['mail_server'], app.config['mail_port'])
            ,fromaddr='no-reply@' + app.config['mail_server']
            ,toaddrs=app.config['admins'] 
            ,subject='Microblog Failure'
            ,credentials=auth
            ,secure=secure
        )
# 记录日志到文件
if not app.debug:
    if not os.path.exists('logs'): # TODO 理解
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')
    
from  app import routes,models, errors



