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
    2、校验数据是否为空
    3、校验手机号是否合法
    4、生成短信验证码
    5、保存短信验证码
    6、发送短信验证码
    7、响应
    :return:
    """
    # data = request.form
    # phone = data.get('phone')

    # dj = request.json
    # print(dj)

    # da = request.data.decode()
    # print(da)

    data = request.get_data()
    json_data = json.loads(data)
    phone = json_data['phone']

    print("phone:", phone)

    if not all([phone]):
        return jsonify(msg="手机号不能为空")
    phone_match = re.match(r'1[3456789][\d]{9}', phone)

    if not phone_match:
        return jsonify(msg="无效的手机号码")

    msg_code = '%04d' % random.randint(0, 9999)

    try:
        redis_store.set(phone, msg_code, 3600)
    except Exception as e:
        logging.error(e)
        return jsonify(msg="验证码错误，请重新请求")

    # ccp = CCP()
    # ret = ccp.send_template_sms(phone, [msg_code, 1], 1)
    # if ret == -1:
    #     return jsonify(msg="验证码发送失败")
    return jsonify(msg=msg_code)
