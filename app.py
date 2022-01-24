import config
from flask import Flask
from flask_migrate import Migrate
from exts import db
# 导入模型关联APP
from models import auth

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

migrate = Migrate(app, db)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
