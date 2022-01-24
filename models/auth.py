# -*- coding: utf-8 -*-
# FileName  : auth.py
# Author    : shiqianlong
import shortuuid
from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash


class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(100), primary_key=True, default=shortuuid.uuid)
    email = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    _password = db.Column(db.String(200), nullable=False)
    avatar = db.Column(db.String(100), comment='头像')
    signature = db.Column(db.String(100), comment='签名')
    join_time = db.Column(db.DateTime, default=datetime.now, comment='加入时间')
    is_staff = db.Column(db.Boolean, default=False, comment='是否员工')
    is_active = db.Column(db.Boolean, default=True, comment='是否可用')

    def __init__(self, *args, **kwargs):
        if 'password' in kwargs:
            self.password = kwargs.get('password')
            kwargs.pop('password')
            super(UserModel, self).__init__(*args, **kwargs)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, newpwd):
        self._password = generate_password_hash(newpwd)
