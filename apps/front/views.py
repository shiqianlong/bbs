# -*- coding: utf-8 -*-
# FileName  : views.py
# Author    : shiqianlong
import string, random, time, os
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
    g,
    jsonify,
    url_for
)
from flask_mail import Message
from flask_avatars import Identicon
from exts import mail, cache, db
from utils import restful
from utils.captcha import Captcha
from .forms import RegisterForm, LoginForm, UploadImageForm, ProfileEditForm
from models.auth import UserModel
from models.post import BoardModel
from .decorators import login_required

bp = Blueprint('front', __name__, url_prefix='/')


@bp.post('/profile/edit')
@login_required
def edit_profile():
    form = ProfileEditForm(request.form)
    if form.validate():
        signature = form.signature.data
        g.user.signature = signature
        db.session.commit()
        return restful.ok()
    else:
        return restful.params_error(message=form.messages[0])


@bp.post('/avatar/upload')
@login_required
def upload_avatar():
    form = UploadImageForm(request.files)
    if form.validate():
        image = form.image.data
        _, suffix_name = os.path.splitext(image.filename)
        filename = md5((g.user.email + str(time.time())).encode('utf-8')).hexdigest() + suffix_name
        image_path = os.path.join(current_app.config['AVATARS_SAVE_PATH'], filename)
        image.save(image_path)
        g.user.avatar = filename
        db.session.commit()
        return restful.ok(data={'avatar': filename})
    else:
        return restful.params_error(message=form.messages[0])


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


@bp.route('/setting')
@login_required
def setting():
    # {{ avatars.gravatar(email_hash) }}
    email_hash = md5((g.user.email).encode('utf-8')).hexdigest()
    return render_template('front/setting.html', email_hash=email_hash)


@bp.route('/logout')
def logout():
    # 用户退出
    session.clear()
    return redirect('/')


@bp.route('/')
def index():
    boards = BoardModel.query.order_by(BoardModel.priority.desc()).all()
    return render_template('front/index.html', boards=boards)


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
            identicon = Identicon()
            filenames = identicon.generate(text=md5(email.encode('utf-8')).hexdigest())
            avatar = filenames[2]
            user = UserModel(email=email, username=username, password=password, avatar=avatar)
            db.session.add(user)
            db.session.commit()
            return restful.ok()
        else:
            return restful.params_error(form.messages[0])


@bp.route('/post/public', methods=['GET', 'POST'])
@login_required
def public_post():
    # 发布贴子
    if request.method == 'GET':
        boards = BoardModel.query.order_by(BoardModel.priority.desc()).all()
        return render_template('front/public_post.html', boards=boards)


@bp.post('/post/image/upload')
@login_required
def post_image_upload():
    # 在富文本编辑器中上传图片
    form = UploadImageForm(request.files)
    if form.validate():
        image = form.image.data
        _, suffix_name = os.path.splitext(image.filename)
        filename = md5((g.user.email + str(time.time())).encode('utf-8')).hexdigest() + suffix_name
        image_path = os.path.join(current_app.config['POST_SAVE_PATH'], filename)
        image.save(image_path)
        return jsonify(
            {"errno": 0,
             'data': [{'url': url_for('media.get_post_image', filename=filename), 'alt': filename, 'href': ''}]})
    else:
        return restful.params_error(message=form.messages[0])
