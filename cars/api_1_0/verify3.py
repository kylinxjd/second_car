import json
import logging
import re, random

from flask import request, jsonify
from cars.libs.yuntongxun.sms import CCP

from . import api
from cars import redis_store


@api.route('/smgcode', methods=['POST'])
def sendMsgCode():
    """
    1、获取参数
    2、校验数据空
    3、校验手机号
    4、生成验证码
    5、保存短信验证码
    6、发送短信验证码
    7、响应
    :return:
    """
    phone = request.json.get('phone')

    if not phone:
        return jsonify(errormsg="手机号不能为空")

    pmatch = re.match(r'1[3456789][\d]{9}', phone)
    if not pmatch:
        return jsonify(errormsg="手机号错误")

    msg_code = "%04d" % random.randint(0, 9999)

    try:
        redis_store.set(phone, msg_code, 3600)
    except:
        return jsonify(errormsg="验证码保存错误")

    return jsonify(msg=msg_code)