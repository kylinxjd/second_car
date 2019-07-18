from flask import Blueprint

# 创建蓝图
api = Blueprint('api_1_0', __name__, template_folder="templates", static_folder="static")

# 注册本蓝图的视图文件
from . import register, verify, cars