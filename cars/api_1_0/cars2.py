from flask import request, render_template, jsonify

from cars import db
from cars.api_1_0 import api
from cars.models import CarImage, Car
from cars.utils import constants
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
            return jsonify(errmsg="数据不完整",errcode=constants.IMCOMPLETE_DATA)
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


@api.route('/upload_file2', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return render_template('upload.html')
    else:
        # 获取前端数据
        file = request.files.get('file')
        car_id = request.form.get('car_id')
        # 校验数据
        if not all([file, car_id]):
            return jsonify(errmsg="数据不完整", errcode=constants.IMCOMPLETE_DATA)
        # 获取图片
        try:
            file_binary = file.read()
        except:
            return jsonify(errmsg="数据不完整", errcode=constants.GET_IMAGE_ERROR)

        # 查询车和车对应的图片
        car = Car.query.get(car_id)
        car_imgs = CarImage.query.filter_by(car_id=car_id).all()
        # 校验车
        if not car:
            return jsonify(errmsg="车不存在", errcode=constants.DATABASE_READ_ERROR)
        # 校验图片数量
        if len(car_imgs) >= 30:
            return jsonify(errmsg="图片已达上限", errcode=constants.IMAGE_DB_FULL)
        # 上传图片
        try:
            ret, res = qiniu_upload_file(file_binary)
            file_url = ret.get('key')
        except:
            return jsonify(errmsg="上传失败", errcode=constants.IMAGE_UPLOAD_ERROR)
        # 保存数据
        try:
            carimgobj = CarImage(car_id=car_id, url=file_url)
            db.session.add(carimgobj)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify(errmsg="数据保存失败", errcode=constants.DATA_SAVE_ERROR)

        return jsonify(msg='上传成功')


@api.route('/carlist2')
def carlist():
    brand = request.args.get('brand')
    carstyle = request.args.get('carstyle')

    car_list = Car.query.all()
    ret_data = []

    if not brand:
        # 不限品牌
        if not carstyle:
            # 不限车型
            for car in car_list:
                dic_info = car.to_list_dict()
                ret_data.append(dic_info)
            return jsonify(msg='不限品牌不限车型', data=ret_data, count=len(ret_data))
        else:
            # 限车型
            for car in car_list:
                if car.brand.car_style == carstyle:
                    dic_info = car.to_list_dict()
                    ret_data.append(dic_info)
            return jsonify(msg='不限品牌限车型', data=ret_data, count=len(ret_data))
    else:
        # 限品牌
        if not carstyle:
            # 不限车型
            for car in car_list:
                if car.brand.name == brand:
                    dic_info = car.to_list_dict()
                    ret_data.append(dic_info)
            return jsonify(msg='限品牌不限车型', data=ret_data, count=len(ret_data))
        else:
            # 限车型
            for car in car_list:
                if car.brand.name == brand and car.brand.car_style == carstyle:
                    dic_info = car.to_list_dict()
                    ret_data.append(dic_info)
            return jsonify(msg='限品牌限车型', data=ret_data, count=len(ret_data))


@api.route('/car/detail')
def car_detail():
    car_id = request.args.get('car_id')
    if not car_id:
        return jsonify(msg="获取car_id失败")
    car = Car.query.get(car_id)
    if not car:
        return jsonify(msg="没有该车")
    car_dict = car.to_detail_dict()
    return jsonify(data=car_dict)
