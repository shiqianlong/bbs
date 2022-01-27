import config
from flask import Flask
from flask_migrate import Migrate
from exts import db, mail, cache, csrf, avatars
# 导入模型关联APP
from models import auth
from apps.front import front_bp
from apps.media import media_bp
from bbs_celery import make_celery

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)
mail.init_app(app)
cache.init_app(app)
csrf.init_app(app)
avatars.init_app(app)

mycelery = make_celery(app)

migrate = Migrate(app, db)

# 注册蓝图
app.register_blueprint(front_bp)
app.register_blueprint(media_bp)

if __name__ == '__main__':
    app.run()
