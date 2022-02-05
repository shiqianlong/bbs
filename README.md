## ORM模型映射到数据库
1. `migrate = Migrate(app,db)`
2. 初始化迁移仓库：flask db init
3. 将orm模型生成迁移脚本：flask db migrate
4. 运行迁移脚本：flask db upgrade

## celery使用
`pip install celery,gevent,redis
`
- win下使用：`celery -A app.mycelery worker --loglevel=info -P gevent`
- Linux下使用：`celery -A app.mycelery worker --loglevel=info`

## CSRF攻击防御
`pip install flask-wtf`
