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
from flask_paginate import get_page_parameter, Pagination
from flask_jwt_extended import create_access_token
from sqlalchemy import func
from exts import mail, cache, db
from utils import restful
from utils.captcha import Captcha
from .forms import (
    RegisterForm,
    LoginForm,
    UploadImageForm,
    ProfileEditForm,
    PublicPostForm,
    PublicCommentForm
)
from models.auth import UserModel
from models.post import BoardModel, PostModel, CommentModel
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
    sort = request.args.get('st', type=int, default=1)
    board_id = request.args.get('bd', type=int, default=None)
    boards = BoardModel.query.order_by(BoardModel.priority.desc()).all()
    post_query = None
    if sort == 1:
        # 按照时间顺序将贴子降序排列
        post_query = PostModel.query.order_by(PostModel.create_time.desc(), PostModel.id.desc())
    else:
        # 按照1.评论数量降序 2.贴子时间降序 将贴子降序排列
        post_query = db.session.query(PostModel).outerjoin(CommentModel).group_by(PostModel.id).order_by(
            func.count(CommentModel.id).desc(), PostModel.create_time.desc(), PostModel.id.desc())
    if board_id:
        post_query = post_query.filter(PostModel.board_id == board_id)
    total = post_query.count()
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * current_app.config['PER_PAGE_COUNT']
    end = start + current_app.config['PER_PAGE_COUNT']
    posts = post_query.slice(start, end)

    pagination = Pagination(bs_version=3, page=page, total=total, prev_label='上一页', next_label='下一页')
    context = {
        'boards': boards,
        'posts': posts,
        'pagination': pagination,
        'st': sort,
        'bd': board_id
    }
    return render_template('front/index.html', **context)


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
            token = ''
            if user.is_staff:
                token = create_access_token(identity=user.id)
            return restful.ok(data={'token': token})
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
    else:
        form = PublicPostForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            try:
                board = BoardModel.query.get(board_id)
            except Exception as e:
                return restful.params_error(message='板块不存在！')
            post_model = PostModel(title=title, content=content, board=board, author=g.user)
            db.session.add(post_model)
            db.session.commit()
            return restful.ok(data={'id': post_model.id})
        else:
            return restful.params_error(message=form.messages[0])


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


@bp.get('/post/detail/<int:post_id>')
def post_detail(post_id):
    try:
        post_model = PostModel.query.get(post_id)
    except Exception as e:
        return '404'
    if not post_model:
        return '<h1>404您的文章不存在！</h1>'
    comment_count = CommentModel.query.filter_by(post_id=post_id).count()
    context = {
        'post': post_model,
        'comment_count': comment_count
    }
    return render_template('front/post_detail.html', **context)


@bp.post('/comment')
@login_required
def public_comment():
    form = PublicCommentForm(request.form)
    if form.validate():
        content = form.content.data
        post_id = form.post_id.data
        post_model = PostModel.query.get(post_id)
        if not post_model:
            return restful.params_error(message='该贴子不存在')
        comment = CommentModel(content=content, post_id=post_id, author_id=g.user.id)
        db.session.add(comment)
        db.session.commit()
        return restful.ok()
    else:
        return restful.params_error(message=form.messages[0])
