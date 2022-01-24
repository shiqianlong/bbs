# -*- coding: utf-8 -*-
# FileName  : config.py
# Author    : shiqianlong
'''
使用时请先配置pw文件中的相关密码信息
'''
import pw

DB_USERNAME = 'root'
DB_PASSWORD = 'root'
DB_HOST = '127.0.0.1'
DB_PORT = '3306'
DB_NAME = 'zlbbs'

DB_URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8mb4' % (DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

SQLALCHEMY_DATABASE_URI = DB_URI
# 是否跟踪修改
SQLALCHEMY_TRACK_MODIFICATIONS = False

'enzfqgeerseideib'
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
