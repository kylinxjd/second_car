from flask import render_template, session, jsonify, request

from cars import redis_store
from cars.models import User, Car
from cars.utils import constants
from cars.utils.login_required import login_required
from . import user


@user.route('/userhistory')
@login_required
def userhistory():
    return render_template('userhistory.html')


@user.route('/userreduce')
@login_required
def userreduce():
    return render_template('userreduce.html')


@user.route('/userstore')
@login_required
def userstore():
    return render_template('userstore.html')


@user.route('/user_collection', methods=['GET', 'POST'])
@login_required
def user_collection():
    if request.method == 'GET':

        return render_template('userstore.html')
        # user_id = session.get('user_id')
        # if not user_id:
        #     return jsonify(errmsg="用户没有登录", errcode=constants.WITHOUT_LOGIN)
        # user_obj = User.query.get(user_id)
        # if not user_obj:
        #     return jsonify(errmsg="数据库读取错误", errcode=constants.DATABASE_READ_ERROR)
        # ret_data = []
        # car_collects = user_obj.cars_collect
        # for car in car_collects:
        #     car_dict = car.to_list_dict()
        #     ret_data.append(car_dict)
        # return jsonify(data=ret_data, count=len(ret_data))
    else:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify(errmsg="用户没有登录", errcode=constants.WITHOUT_LOGIN)
        user_obj = User.query.get(user_id)
        if not user_obj:
            return jsonify(errmsg="数据库读取错误", errcode=constants.DATABASE_READ_ERROR)
        ret_data = []
        car_collects = user_obj.cars_collect
        for car in car_collects:
            car_dict = car.to_detail_dict()
            ret_data.append(car_dict)
        return jsonify(data=ret_data, count=len(ret_data))


@user.route('/user_history', methods=['GET', 'POST'])
def user_history():
    if request.method == 'GET':
        user_id = session.get('user_id')
        user_history = 'history_%s' % user_id
        try:
            data = redis_store.lrange(user_history, 0, -1)
        except:
            return jsonify(msg="尚无浏览数据")
        ret_data = []
        for d in data:
            try:
                car_id = d.decode()
                carobj = Car.query.get(car_id)
                cardicinfo = carobj.to_detail_dict()
                ret_data.append(cardicinfo)
            except:
                print("asd")
        return jsonify(data=ret_data)

    else:
        user_id = session.get('user_id')
        user_history = 'history_%s' % user_id
        try:
            data = redis_store.lrange(user_history, 0, -1)
        except:
            return jsonify(msg="尚无浏览数据")
        ret_data = []
        for d in data:
            try:
                car_id = d.decode()
                carobj = Car.query.get(car_id)
                cardicinfo = carobj.to_detail_dict()
                ret_data.append(cardicinfo)
            except:
                print("asd")
        return jsonify(data=ret_data)

