# -*- coding: utf-8 -*-
# FileName  : commands.py
# Author    : shiqianlong
import random
from exts import db
from models.post import BoardModel, PostModel
from models.auth import UserModel


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


def create_test_posts():
    boards = list(BoardModel.query.all())
    for x in range(100):
        title = '我是标题%d' % x
        content = '我是内容%d' % x
        author = UserModel.query.first()
        index = random.randint(0, len(boards) - 1)
        board = boards[index]
        post_model = PostModel(title=title, content=content, author=author, board=board)
        db.session.add(post_model)
    db.session.commit()
    print('测试贴子添加成功！')
