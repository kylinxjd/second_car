import json

from flask import request, render_template, jsonify, session, g

from cars import db, redis_store
from cars.api_1_0 import api
from cars.models import CarImage, Car, Brand, User
from cars.utils import constants
from cars.utils.login_required import login_required
from cars.utils.qiniu_upload import qiniu_upload_file


@api.route('/upload', methods=['GET'])
def upload():
    return render_template('upload.html')


@api.route('/car/changeprice', methods=['GET', 'POST'])
def change():
    if request.method == 'GET':
        return render_template('change_price.html')
    else:
        car_id = request.json.get('car_id')
        new_price = request.json.get('new_price')
        # print(car_id)
        # print(new_price)
        # print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        if not all([car_id, new_price]):
            return jsonify(errmsg="数据不完整", errcode=constants.IMCOMPLETE_DATA)
        try:
            car_obj = Car.query.get(car_id)
        except Exception as e:
            return jsonify(errmsg="数据库读取失败", errcode=constants.DATABASE_READ_ERROR)
        if not car_obj:
            return jsonify(errmsg="该车不存在", errcode=constants.DATA_NOT_FOUND)
        car_obj.price = new_price
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify(errmsg="更新失败", errcode=constants.DATA_SAVE_ERROR)
        return jsonify(msg='更新成功')


@api.route('/upload_file', methods=['POST'])
def upload_file():
    # todo 获取前端上传的图片
    file = request.files
    data = request.form
    # data = request.json
    try:
        file_binary = file['file'].read()
        file_name = file['file']
        car_id = data.get('car_id')
        print('获取的前端数据', file_name, car_id)
    except Exception as e:
        return jsonify(errmsg="请上传图片",
                       errcode=constants.GET_IMAGE_ERROR)
    # todo 使用自定义文件上传系统上传图片文件
    try:
        ret, res = qiniu_upload_file(file_binary)
        filename = ret.get('key')
        # http://puek1pi1o.bkt.clouddn.com/FgxnUXen216OyNMC4t6zwwQ0HSYU FguAYN5tgMLfOjvssZJR6Ak1Xbla
    except Exception as e:
        return jsonify(errmsg="图片上传失败",
                       errcode=constants.IMAGE_UPLOAD_ERROR)
    # todo 判断数据库是否存在该车
    car = Car.query.get(car_id)
    carimgs = CarImage.query.filter_by(car_id=car_id).all()
    if not car:
        return jsonify(errmsg="该车不存在")
    # todo 判断当前车辆图片是否超过30张
    if len(carimgs) >= 30:
        return jsonify(errmsg="该车图片已达上限", errcode=constants.IMAGE_DB_FULL)
    # todo 将图片url保存到数据库
    try:
        carimg_obj = CarImage(car_id=car_id, url=filename)
        db.session.add(carimg_obj)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(errmsg="数据库存储失败", errcode=constants.IMAGE_DB_FULL)

    # return jsonify(filename=ret.get('key'))
    return jsonify(msg='上传成功')


@api.route('/car/list', methods=['GET', 'POST'])
def carlist():
    brand = request.args.get('brand')
    carstyle = request.args.get('carstyle')

    if not brand:
        if not carstyle:
            # 不限品牌不限车型查找
            car_list = Car.query.all()
            ret_data = []
            for car in car_list:
                dic_info = car.to_list_dict()
                ret_data.append(dic_info)
            print(ret_data)
            return jsonify(msg='不限品牌不限车型查找', data=ret_data, count=len(ret_data))
        else:
            # 不限品牌限车型查找
            ret_data = []

            brand_obj_list = Brand.query.filter_by(car_style=carstyle).all()
            if not brand_obj_list:
                return jsonify(msg='没有找到车')
            for brand_obj in brand_obj_list:
                car_list = brand_obj.cars

                for car in car_list:
                    dic_info = car.to_list_dict()
                    ret_data.append(dic_info)
            print(ret_data)
            return jsonify(msg='不限品牌限车型查找', data=ret_data, count=len(ret_data))
    else:
        # 限品牌不限车型
        if not carstyle:
            ret_data = []

            brand_obj_list = Brand.query.filter_by(name=brand).all()
            if not brand_obj_list:
                return jsonify(msg='没有找到车')
            for brand_obj in brand_obj_list:
                car_list = brand_obj.cars

                for car in car_list:
                    dic_info = car.to_list_dict()
                    ret_data.append(dic_info)
            print(ret_data)
            return jsonify(msg='限品牌不限车型', data=ret_data, count=len(ret_data))
        else:
            # 限品牌限车型
            ret_data = []

            brand_obj = Brand.query.filter_by(name=brand, car_style=carstyle).first()
            if not brand_obj:
                return jsonify(msg='没有找到车')
            car_list = brand_obj.cars

            for car in car_list:
                dic_info = car.to_list_dict()
                ret_data.append(dic_info)
            print(ret_data)
            return jsonify(msg='限品牌限车型', data=ret_data, count=len(ret_data))

@api.route('/cars/show')
def cars_show():
    return render_template('cars_show.html')


@api.route('/car/show')
def car_show():
    car_id = request.args.get('id')
    return render_template('car_detail.html', carid=car_id)


@api.route('/car/detail', methods=['GET', 'POST'])
def car_detail():
    """
    todo 1、获取用户id
    todo 2、校验id是否为空
    todo 3、判断用户登录状态
    todo    登录则保存浏览记录
    todo    否则不保存
    todo 4、从redis查询记录
            有记录就取出返回
    todo    没有则从数据库取出数据返回给前端
    :return:
    """
    car_id = request.args.get('id')

    if not car_id:
        return jsonify(errmsg='数据返回错误', errcode=404)

    user_id = session.get('user_id')

    if not user_id:
        print("用户未登录")
    else:
        print("用户已登录")
        try:
            history_key = "history_%s" % user_id
            redis_store.lrem(history_key, 0, car_id)
            redis_store.lpush(history_key, car_id)
        except:
            return jsonify(errmsg="记录保存失败", error=constants.REDIS_SAVE_ERROR)

    # car = Car.query.get(car_id)
    # car_dict = car.to_detail_dict()

    # 查看redis是否有记录
    car_redis = redis_store.get("car_%s" % car_id)
    if not car_redis:
        # 没有，从数据库查找
        car = Car.query.get(car_id)
        car_dict = car.to_detail_dict()
        # 存入Reids
        try:
            car_dict_string = json.dumps(car_dict)
            redis_store.set("car_%s" % car_id, car_dict_string)
        except Exception as e:
            print(e)
    else:
        # 有记录
        car_dict = json.loads(car_redis.decode())

    return jsonify(data=car_dict)


@api.route('/brand/list')
def brandlist():
    brand_list = Brand.query.all()
    ret_data = []
    for brand in brand_list:
        dicInfo = brand.to_dict()
        ret_data.append(dicInfo)
    return jsonify(count=len(ret_data), msg='品牌列表页', data=ret_data)


@api.route('/car/collection', methods=['GET', 'POST'])
@login_required
def collection():

    # car_id = request.json.get('car_id')
    car_id = request.args.get('car_id')
    if not car_id:
        return jsonify(msg="asd")

    user_id = session.get('user_id')

    user_obj = User.query.get(user_id)
    car_obj = Car.query.get(car_id)
    if not all([user_obj, car_obj]):
        return jsonify(msg="收藏失败")
    user_obj.cars_collect.append(car_obj)
    # db.session.add(user_obj)
    db.session.commit()

    return jsonify(msg="收藏成功")


