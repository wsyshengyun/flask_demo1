from app import app
from app import db 
from app.models import *   # 解决数据库无法适移的问题


# 添加一个shell上下文
@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'User':User, 'Post':Post, 'a':4}
