import json,logging
from flask import render_template, request, jsonify, session

from . import api
from cars import redis_store, db
from cars.models import User


@api.route('/login')
def login():
    return render_template('login.html')

@api.route('/register', methods=['POST'])
def register():
    """
    1、获取数据
    2、校验空
    3、校验正确性
    4、查找redis的验证码
    5、比较验证码
    6、查找用户
        已存在
            登录成功
        没有
            添加用户
    7、保存session
    :return:
    """
    data = request.json
    phone = data.get('phone')
    code_input = data.get('msgcode')

    if not all([phone, code_input]):
        return jsonify(errormsg='数据不完整')

    code_redis = redis_store.get(phone).decode()

    if code_input != code_redis:
        return jsonify(errormsg='验证码错误')

    user_obj = User.query.filter_by(phone=phone).first()
    if not user_obj:
        user_obj = User(phone=phone)
        try:
            db.session.add(user_obj)
            db.session.commit()
        except Exception as e:
            return jsonify(errormsg='用户添加失败')


    session['user_id'] = user_obj.id
    session['user_phone'] = user_obj.phone

    return jsonify(msg='登录成功')