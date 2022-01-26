# -*- coding: utf-8 -*-
# FileName  : forms.py
# Author    : shiqianlong
from wtforms import Form, ValidationError
from wtforms.validators import Email, Length, EqualTo
from wtforms.fields import StringField
from flask import request
from models.auth import UserModel
from exts import cache


class BaseForm(Form):
    @property
    def messages(self):
        message_list = []
        if self.errors:
            for errors in self.errors.values():
                message_list.extend(errors)
        return message_list


class RegisterForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确格式邮箱！')])
    email_captcha = StringField(validators=[Length(6, 6, message='请输入正确格式的邮箱验证码！')])
    username = StringField(validators=[Length(3, 20, message='请输入正确格式的用户名3-20字符！')])
    password = StringField(validators=[Length(6, 20, message='请输入正确格式密码！')])
    repeat_password = EqualTo('password', message='两次密码输入不一致！')
    graph_captcha = StringField(validators=[Length(4, 4, message='请输入正确格式图像验证码！')])

    def validate_email(self, field):
        email = field.data
        email = UserModel.query.filter_by(email=email).first()
        if email:
            raise ValidationError(message='该邮箱以存在')

    def validate_captcha(self, field):
        email_captcha = field.data
        email = self.email.data
        email_captcha_redis = cache.get(email)
        if not email_captcha_redis or email_captcha_redis.lower() != email_captcha.lower():
            raise ValidationError(message='邮箱验证码错误')

    def validate_graph_captcha(self, field):
        graph_captcha = field.data
        key = request.cookies.get('_graph_captcha_key', '')
        print(key)
        graph_captcha_redis = cache.get(key)
        print('取出的图像验证码%s: ' % graph_captcha_redis)
        if not graph_captcha_redis or graph_captcha_redis.lower() != graph_captcha.lower():
            raise ValidationError(message='图像验证码错误')