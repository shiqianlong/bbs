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
    make_response,
    session,
    redirect,
    g
)
from flask_mail import Message
from exts import mail, cache, db
from utils import restful
from utils.captcha import Captcha
from .forms import RegisterForm, LoginForm
from models.auth import UserModel

bp = Blueprint('front', __name__, url_prefix='/')


@bp.before_request
# 钩子方法，在进入视图前处理
def front_before_request():
    if 'user_id' in session:
        user_id = session.get('user_id')
        user = UserModel.query.get(user_id)
        setattr(g, 'user', user)


@bp.context_processor
# 上下文处理器，视图层处理后经过这里
def front_content_process():
    if hasattr(g, 'user'):
        return {'user': g.user}
    else:
        return {}


@bp.route('/logout')
def logout():
    # 用户退出
    session.clear()
    return redirect('/')


@bp.route('/')
def index():
    return render_template('front/index.html')


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
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                return restful.params_error(message='该邮箱未注册')
            if not user.check_password(password):
                return restful.params_error(message='邮箱或密码错误')
            if not user.is_active:
                return restful.params_error(message='该账号已封存，请联系管理员')
            if remember == 1:
                session.permanent = True
            session['user_id'] = user.id
            return restful.ok()
        else:
            return restful.permission_error(message=form.messages[0])


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
