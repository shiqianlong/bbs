# -*- coding: utf-8 -*-
# FileName  : config.py
# Author    : shiqianlong

DB_USERNAME = 'root'
DB_PASSWORD = 'root'
DB_HOST = '127.0.0.1'
DB_PORT = '3306'
DB_NAME = 'zlbbs'

DB_URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8mb4' % (DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

SQLALCHEMY_DATABASE_URI = DB_URI
# 是否跟踪修改
SQLALCHEMY_TRACK_MODIFICATIONS = False
