import functools
import logging

from flask import session, jsonify, g

from cars.utils import constants


def login_required(func):
    @functools.wraps(func) # 修饰内层函数，防止当前装饰器去修改被装饰函数的属性
    def inner(*args, **kwargs):
        # 从session获取用户信息，如果有，则用户已登录，否则没有登录
        user_id = session.get('user_id')
        print("session user_id:", user_id)
        if not user_id:
            return jsonify(errcode=constants.WITHOUT_LOGIN,
                           err="用户未登录")
        else:
            # 已经登录的话 g变量保存用户信息，相当于flask程序的全局变量
            g.user_id = user_id
            return func(*args, **kwargs)
    return inner




