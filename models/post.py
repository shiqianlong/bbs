# -*- coding: utf-8 -*-
# FileName  : post.py
# Author    : shiqianlong

# 贴子模型
from datetime import datetime
from exts import db


class BoardModel(db.Model):
    # 板块模型
    __tablename__ = 'board'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True, comment='板块名称')
    priority = db.Column(db.Integer, default=1, comment='优先级')
    create_time = db.Column(db.DateTime, default=datetime.now, comment='创建时间')


class PostModel(db.Model):
    # 贴子模型
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False, comment='贴子标题')
    content = db.Column(db.Text, nullable=False, comment='内容')
    create_time = db.Column(db.DateTime, default=datetime.now, comment='创建时间')

    board_id = db.Column(db.Integer, db.ForeignKey('board.id'), comment='所属板块id')
    author_id = db.Column(db.String(100), db.ForeignKey('user.id'), comment='所属作者id')

    # 使用反向引用(通过板块查看所属所有贴子): board.posts
    board = db.relationship('BoardModel', backref=db.backref('posts'))
    author = db.relationship('UserModel', backref=db.backref('posts'))


class BannerModel(db.Model):
    # 轮播图模型
    __tablename__ = 'banner'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False, comment='轮播图名称')
    image_url = db.Column(db.String(250), nullable=False, comment='图片链接')
    link_url = db.Column(db.String(250), nullable=False, comment='跳转链接')
    priority = db.Column(db.Integer, default=0, comment='优先级')
    create_time = db.Column(db.DateTime, default=datetime.now, comment='创建时间')


class CommentModel(db.Model):
    # 评论模型
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False, comment='评论内容')
    create_time = db.Column(db.DateTime, default=datetime.now, comment='创建时间')

    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), comment='所属贴子id')
    author_id = db.Column(db.String(100), db.ForeignKey("user.id"), nullable=False, comment='所属作者id')

    post = db.relationship("PostModel", backref=db.backref('comments', order_by="CommentModel.create_time.desc()",
                                                           cascade="delete, delete-orphan"))
    author = db.relationship("UserModel", backref='comments')
