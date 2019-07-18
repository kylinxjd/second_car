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


@api.route('/upload_file4', methods=['GET', 'POST'])
def upload_file():
    car_id = request.form.get('car_id')
    file = request.files.get('file')

    if not all([car_id, file]):
        return jsonify(m='not complete')

    try:
        file_binary = file.read()
    except:
        return jsonify(m='upload failed')

    car = Car.query.get(car_id)
    carimgs = CarImage.query.filter_by(car_id=car_id).all()

    if not car:
        return jsonify(m="该车不存在")

    if len(carimgs) >= 30:
        return jsonify(m='图片已达上限')
    try:
        ret, res = qiniu_upload_file(file_binary)
    except:
        return jsonify(m='shangchuanshibai')

    imgurl = ret.get('key')

    carimgobj = CarImage(car_id=car_id, url=imgurl)

    try:
        db.session.add(carimgobj)
        db.commit()
    except:
        db.session.rollback()
        return jsonify(m='baocunshibai')

    return jsonify(msg='上传成功')


@api.route('/car/detail')
def detail_car():
    car_id = request.args.get('id')
    if not car_id:
        return jsonify(m='id获取失败')
    car = Car.query.get(car_id)
    if not car:
        return jsonify(m='获取车失败')
    return jsonify(m=car.to_detail_dict())


@api.route('/car/list')
def cars_list():
    brand = request.args.get('brand')
    carstyle = request.args.get('carstyle')

    ret_data = []
    cars = Car.query.all()

    if not brand:
        if not carstyle:
            for car in cars:
                car_dic = car.to_list_dict()
                ret_data.append(car_dic)
            return jsonify(m=ret_data)
        else:
            for car in cars:
                if car.brand.car_style == carstyle:
                    car_dic = car.to_list_dict()
                    ret_data.append(car_dic)
            return jsonify(m=ret_data)
    else:
        if not carstyle:
            for car in cars:
                if car.brand.name == brand:
                    car_dic = car.to_list_dict()
                    ret_data.append(car_dic)
            return jsonify(m=ret_data)
        else:
            for car in cars:
                if car.brand.car_style == carstyle and car.brand.name == brand:
                    car_dic = car.to_list_dict()
                    ret_data.append(car_dic)
            return jsonify(m=ret_data)

