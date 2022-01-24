import config
from flask import Flask
from flask_migrate import Migrate
from exts import db, mail
# 导入模型关联APP
from models import auth
from apps.front import front_bp

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)

migrate = Migrate(app, db)
# 注册蓝图
app.register_blueprint(front_bp)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
