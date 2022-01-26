# -*- coding: utf-8 -*-
# FileName  : views.py
# Author    : shiqianlong
import string, random
from io import BytesIO
from hashlib import md5
from flask import (
    Blueprint,
    request,
    render_template,
    current_app,
    make_response
)
from flask_mail import Message
from exts import mail, cache, db
from utils import restful
from utils.captcha import Captcha
from .forms import RegisterForm
from models.auth import UserModel

bp = Blueprint('front', __name__, url_prefix='/')


@bp.route('/graph/captcha')
def graph_captcha():
    captcha, image = Captcha.gene_graph_captcha()
    # 生成一个验证码对应的key放入cookie中
    key = md5(captcha.encode('utf-8')).hexdigest()
    out = BytesIO()
    image.save(out, 'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    resp.set_cookie('_graph_captcha_key', key, max_age=3600)
    cache.set(key, captcha)
    return resp


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
    print(captcha)
    return restful.ok()


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('front/login.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('front/register.html')
    else:
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return restful.ok()
        else:
            return restful.params_error(form.messages[0])
