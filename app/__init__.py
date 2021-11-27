from os import truncate
from  flask import Flask 
from config import Config


app = Flask(__name__)
app.config.from_object(Config) # 此app就是Flask；
app.debug=True

from  app import routes



