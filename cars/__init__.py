import redis
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
import logging
from logging.handlers import RotatingFileHandler

# from cars.user import user
# from cars.api_1_0 import api

from config import config

redis_store = None

db = SQLAlchemy()
# csrf = CSRFProtect()

# 日志设置
logging.basicConfig(level=logging.DEBUG)
# 创建日志记录器，指明保存路径,文件大小，保存日志上限
file_log_handler = RotatingFileHandler(filename='logs/log',
                                       maxBytes=1024 * 1024,
                                       backupCount=10,
                                       encoding='utf-8')
# 日志格式
log_formater = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(lineno)d %(message)s')
# 将日志记录器指定日志格式
file_log_handler.setFormatter(log_formater)
# 为全局的日志工作对象添加日志记录器
logging.getLogger().addHandler(file_log_handler)


def create_app(config_name):
    # 根据运行的模式加载不同的配置对象
    app = Flask(__name__)

    app.config.from_object(config[config_name])

    # 数据库句柄app
    db.init_app(app=app)
    # session关联app
    Session(app)

    # csrf.init_app(app=app)

    global redis_store
    redis_store = redis.StrictRedis(host=config[config_name].REDIS_HOST,
                                    port=config[config_name].REDIS_PORT)

    # logging.debug("debug模式")
    # 注册蓝图
    from cars.api_1_0 import api
    from user import user
    app.register_blueprint(api, url_prefix='/api/v1.0')
    app.register_blueprint(user, url_prefix='/user')

    return app
