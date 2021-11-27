from os import truncate
from  flask import Flask 
from config import Config
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
# from models import *



app = Flask(__name__)
app.config.from_object(Config) # 此app就是Flask；
app.debug=True
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from  app import routes



