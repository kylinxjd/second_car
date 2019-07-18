from flask import Blueprint
# 创建蓝图
user = Blueprint('user', __name__, template_folder="templates", static_folder="static")
# 注册本蓝图的视图文件
from . import userinfo, login
