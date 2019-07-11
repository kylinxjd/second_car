import json
import logging

from flask import render_template, request, jsonify, session

from . import api
from cars import redis_store, db
from cars.models import User
from cars.utils.login_required import login_required


@api.route('/login')
def login():
    return render_template('login.html')


@api.route('/index')
@login_required
def index():
    return "<h1>index</h1>"


@api.route('/logout', methods=['DELETE'])
@login_required
def logout():
    session.pop('user_id')
    session.pop('user_phone')
    logging.info('用户退出登录')
    return jsonify(msg="logout")


@api.route('/login', methods=['POST'])
def register():
    """
    1、获取前端post过来的数据
    2、校验数据是否为空
    3、校验数据是否合法
    4、获取redis里的验证码
    5、比较用户传递的验证码和redis取出的验证码
    6、判断数据库是否已经存在用户
        如果存在登录
        如果不存在添加用户
    7、添加数据到session
    :return:
    """
    # phone = request.form.get('phone')
    # input_code = request.form.get('msgcode')

    data = request.get_data()
    json_data = json.loads(data)
    phone = json_data['phone']
    input_code = json_data['msgcode']

    if not all([phone, input_code]):
        return jsonify(error_msg="数据不完整")

    redsi_code = redis_store.get(phone).decode()

    if input_code != redsi_code:
        return jsonify(error_msg="验证码错误")

    user_obj = User.query.filter_by(phone=phone).first()
    if not user_obj:
        # 数据库不存在
        user_obj_new = User(phone=phone)
        try:
            db.session.add(user_obj_new)
            db.session.commit()
            user_obj = user_obj_new
        except Exception as e:
            logging.error("数据库添加错误")
            db.session.rollback()
            return jsonify(error_msg="数据库添加错误")

    session['user_id'] = user_obj.id
    session['user_phone'] = user_obj.phone

    return jsonify(msg="登录成功")
