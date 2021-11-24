from  flask import Flask 
from config import Config


app = Flask(__name__)
app.config.from_object(Config) # 此app就是Flask；


from  app import routes



