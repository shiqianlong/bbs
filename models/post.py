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
