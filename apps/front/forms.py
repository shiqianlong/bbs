# -*- coding: utf-8 -*-
# FileName  : forms.py
# Author    : shiqianlong
from wtforms import Form, ValidationError
from wtforms.validators import Email, Length, EqualTo, InputRequired
from wtforms.fields import StringField, IntegerField, FileField
from flask import request
from flask_wtf.file import FileAllowed, FileSize
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


class ProfileEditForm(BaseForm):
    """个人设置页面信息编辑校验"""
    signature = StringField(validators=[Length(min=1, max=50, message="个性签名长度在1-50字之间！")])


class UploadImageForm(BaseForm):
    image = FileField(validators=[FileAllowed(['jpg', 'png', 'jpeg', ], message='图片格式不符合要求'),
                                  FileSize(max_size=1024 * 1024 * 3, message='图片最大不能超过3M')])


class LoginForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确格式邮箱！')])
    password = StringField(validators=[Length(6, 20, message='请输入正确格式密码！')])
    remember = IntegerField()


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


class PublicPostForm(BaseForm):
    # 发布贴子校验
    title = StringField(validators=[Length(1, 200, message='标题字符应在1~20之间')])
    content = StringField(validators=[InputRequired(message='文章内容是必传字段')])
    board_id = IntegerField(validators=[InputRequired(message='板块ID是必传字段')])


class PublicCommentForm(BaseForm):
    # 发布评论校验
    content = StringField(validators=[Length(max=500, message='评论内容不超过500字符！'), InputRequired(message='未填写评论内容')])
    post_id = IntegerField(validators=[InputRequired(message='post_id是必传字段')])
