# -*- coding: utf-8 -*-
# FileName  : config.py
# Author    : shiqianlong
'''
使用时请先配置pw文件中的相关密码信息
'''
import pw
import os
from datetime import timedelta

# session.permanent=True的情况下的过期时间
PERMANENT_SESSION_LIFETIME = timedelta(days=30)

# 本文件所在的文件夹
BASE_DIR = os.path.dirname(__file__)

DB_USERNAME = 'root'
DB_PASSWORD = 'root'
DB_HOST = '127.0.0.1'
DB_PORT = '3306'
DB_NAME = 'zlbbs'

DB_URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8mb4' % (DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

SQLALCHEMY_DATABASE_URI = DB_URI
# 是否跟踪修改
SQLALCHEMY_TRACK_MODIFICATIONS = False

# MAIL_USE_TLS：端口号587
# MAIL_USE_SSL：端口号465
# QQ邮箱不支持非加密方式发送邮件
# 发送者邮箱的服务器地址
MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = 587
MAIL_USE_TLS = True
# MAIL_USE_SSL = True
MAIL_USERNAME = pw.MAIL_USERNAME
MAIL_PASSWORD = pw.MAIL_PASSWORD
MAIL_DEFAULT_SENDER = pw.MAIL_DEFAULT_SENDER

# Celery的redis配置
CELERY_BROKER_URL = pw.celery_redis
CELERY_RESULT_BACKEND = pw.celery_redis

# flask-caching缓存设置
CACHE_TYPE = "RedisCache"
CACHE_DEFAULT_TIMEOUT = 300
CACHE_REDIS_HOST = pw.CACHE_REDIS_HOST
CACHE_REDIS_PORT = pw.CACHE_REDIS_PORT
CACHE_REDIS_PASSWORD = pw.CACHE_REDIS_PASSWORD
CACHE_REDIS_DB = pw.CACHE_REDIS_DB

# 密钥(自定义)
SECRET_KEY = pw.SECRET_KEY

# 头像配置
AVATARS_SAVE_PATH = os.path.join(BASE_DIR, "media", "avatars")

# 富文本编辑器图片上传地址
POST_SAVE_PATH = os.path.join(BASE_DIR, "media", "post")
