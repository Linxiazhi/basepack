# -*-coding: utf-8-*-
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
import time
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy(use_native_unicode='utf8')


# 用户信息
class User(db.Model, UserMixin):
    __tablename__ = 'tb_user'
    id = db.Column(db.Integer, primary_key = True)
    phone = db.Column(db.String(32), index = True, unique = True)
    password_hash = db.Column(db.String(128))
    nickname = db.Column(db.String(128))
    #注册登录信息
    regDate = db.Column(db.TIMESTAMP)
    regID = db.Column(db.String(128))
    lastloginDate = db.Column(db.TIMESTAMP)
    lastloginIP = db.Column(db.String(128))
    # 推送设备标识
    registrationID = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def register_init(self):
        self.regDate = int(time.time())
        self.lastloginDate = int(time.time())

    # 检查手机号是否存在
    @staticmethod
    def verfiy_exist(phone):
        user = User.query.filter_by(phone = phone).first()
        if user is None:
            return False
        else:
            return True

    @staticmethod
    def get_uid(phone):
        user = User.query.filter_by(phone = phone).first()
        if user is None:
            return 0
        else:
            return user.id

    def generate_confirmation_token(self, expiration = 604800):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        return True

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns if c.name != 'password_hash'}

