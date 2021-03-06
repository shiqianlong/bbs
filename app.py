import config
import commands
from flask import Flask
from flask_migrate import Migrate
from exts import db, mail, cache, csrf, avatars, jwt
# 导入模型关联APP
from models import auth
from apps.front import front_bp
from apps.media import media_bp
from apps.cmsapi import cmsapi_bp
from bbs_celery import make_celery

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)
mail.init_app(app)
cache.init_app(app)
csrf.init_app(app)
avatars.init_app(app)
jwt.init_app(app)

mycelery = make_celery(app)

migrate = Migrate(app, db)

# 注册蓝图
app.register_blueprint(front_bp)
app.register_blueprint(media_bp)
app.register_blueprint(cmsapi_bp)

# 注册命令
app.cli.command('greet')(commands.greet)
app.cli.command('init_board')(commands.init_boards)
app.cli.command('create_test_posts')(commands.create_test_posts)

if __name__ == '__main__':
    app.run()
