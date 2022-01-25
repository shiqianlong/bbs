# -*- coding: utf-8 -*-
# FileName  : views.py
# Author    : shiqianlong
import string, random
from flask import (
    Blueprint,
    request,
    render_template,
    current_app
)
from flask_mail import Message
from exts import mail, cache
from utils import restful

bp = Blueprint('front', __name__, url_prefix='/')


@bp.get('/email/captcha')
def email_captcha():
    # /email/captcha?email=xxxx
    email = request.args.get('email')
    if not email:
        return restful.params_error(message='请输入邮箱')
    # 随机六位数字
    source = list(string.digits)
    captcha = ''.join(random.sample(source, 6))
    # message = Message(subject='【子午】注册验证码', recipients=[email], body='【子午】您的验证码是：%s' % captcha)
    # try:
    #     mail.send(message)
    # except Exception as e:
    #     message = '邮件发送发生错误！' + str(e)
    #     print(e)
    #     return jsonify({'code': 500, 'message': message})
    subject = '【子午】注册验证码'
    body = '【子午】您的验证码是：%s' % captcha
    # 使用celery异步发送邮件
    # current_app.celery.send_task('send_mail', (email, subject, body))
    cache.set(email, captcha)

    return restful.ok()


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('front/login.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('front/register.html')
