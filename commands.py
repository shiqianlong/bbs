# -*- coding: utf-8 -*-
# FileName  : commands.py
# Author    : shiqianlong
from exts import db
from models.post import BoardModel


def greet():
    # 通过在终端：flask greet 打印命令
    print('hello flask')


def init_boards():
    board_names = ['Python', 'Flask', 'Django', '前端']
    for index, board_name in enumerate(board_names):
        board = BoardModel(name=board_name, priority=len(board_names) - index)
        db.session.add(board)
    db.session.commit()
    print('板块添加成功')
