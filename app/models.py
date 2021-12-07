# from sqlalchemy.orm import backref
from app import db
from app import  avatars
from app import app
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from app import login
from flask_login import UserMixin
import jwt 
from time import time 



@login.user_loader
def log_user(id):
    return User.query.get(int(id))


# -----------------------------------------------------------
# 添加粉丝机制
# -----------------------------------------------------------
followers = db.Table('followers', 
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
        # backref 返回索引的作用
        # TODO lazy??
        # 这是一对多的关系 在一的那一方添加关系relationship，在多的一方添加外键
    followed = db.relationship(
        'User', secondary=followers
        ,primaryjoin=(followers.c.follower_id == id)
        ,secondaryjoin=(followers.c.followed_id==id)
        ,backref=db.backref('followers', lazy='dynamic')
        ,lazy='dynamic'
    )

    def __repr__(self) -> str:
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        _dict = {'reset_password':self.id, 'exp':time() + expires_in}
        return jwt.encode( _dict
            ,app.config['SECRET_KEY']
            ,algorithm='HS256'
        ).decode('utf-8')
    
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET-KEY']
                ,algorithms=['HS256'])['reset_password']
        except:
            return 
        return User.query.get(id)

    def avatar(self, size='m'):
        """ size: default is 'm', other 's'小号, 'l' 大号 """
        return avatars.default(size=size)
    
    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id
        ).count()>0

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
    
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
    
    def followed_posts(self):
        # return Post.query.join(
        #     followers, (followers.c.followed_id == Post.user_id)
        # ).filter(followers.c.follower_id == self.id).order_by(
        #     Post.timestamp.desc()
        # )
        followed = Post.query.join(
            followers, (followers.c.followed_id==Post.user_id)
        ).filter(followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id = self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
        # 要复习的知识点  Column->db.type, index, default
        # db.ForeignKey
        # TODO String(140)?? 140长度指的是什么

    def __repr__(self):
        return '<Post {}, {}>'.format(self.body, self.user_id)




