# -*- coding: utf-8 -*-
# FileName  : decorators.py
# Author    : shiqianlong
"""
相关装饰器文件
"""
from flask import g, redirect, url_for
from functools import wraps


def login_required(func):
    # 通过判断session中是否存在user_id字段进行判断
    @wraps(func)
    def inner(*args, **kwargs):
        if hasattr(g, 'user'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('front.login'))

    return inner
