from datetime import datetime

from . import db


class BaseModel(object):
    is_delete = db.Column(db.Boolean, default=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class User(BaseModel, db.Model):
    __tablename__ = 'sc_users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=True, unique=True)
    password = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(11), nullable=False)
    id_card = db.Column(db.String(18), nullable=True)
    cars = db.relationship('Car', backref='user')
    order = db.relationship('Order', backref='user')

    def __repr__(self):
        return self.name


class Car(BaseModel, db.Model):
    __tablename__ = 'sc_cars'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('sc_users.id'))
    brand_id = db.Column(db.Integer, db.ForeignKey('sc_brand.id'))
    # 价格
    price = db.Column(db.Integer, nullable=False)
    # 车龄
    age = db.Column(db.Integer, nullable=True)
    # 车型
    vehicle_model = db.Column(db.String(20), nullable=True)
    # 变速箱，0自动，1手动
    gear_box = db.Column(db.Integer, default=1)
    # 里程数
    milage = db.Column(db.DECIMAL(), default=0)
    # 排量
    displacement = db.Column(db.Float)
    # 上牌时间
    car_register_time = db.Column(db.DateTime, default=datetime.now)
    # 车架号
    car_num = db.Column(db.String(50))
    # 颜色
    color = db.Column(db.String(10))
    # 燃油类型
    car_oil = db.Column(db.String(10))
    # 排放标准
    emission_standard = db.Column(db.String(10))
    # 座位数
    seat_num = db.Column(db.Integer)
    # 过户数
    transfer_num = db.Column(db.Integer)
    # 年检
    inspect_annually = db.Column(db.String(10))
    # 交强险
    compulsory_insurance = db.Column(db.String(10))
    # 商业保险
    commercial_annually = db.Column(db.String(10))
    index_image_url = db.Column(db.String(100))
    images = db.relationship('CarImage')

    order = db.relationship('Order', backref='car')

    def __repr__(self):
        return self.id


class CarImage(db.Model):
    __tablename__ = 'sc_car_img'

    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('sc_cars.id'))
    url = db.Column(db.String(100))

    def __repr__(self):
        return self.url


class Brand(db.Model):
    __tablename__ = 'sc_brand'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=True, unique=True)
    # teacher_id = db.Column(db.Integer, db.ForeignKey('tea.id'))
    # 类型
    car_style = db.Column(db.String(50), nullable=True)
    car_style_detail = db.Column(db.String(50), nullable=True)
    cars = db.relationship('Car', backref='brand')

    def __repr__(self):
        return self.name


class Order(BaseModel, db.Model):
    __tablename__ = 'sc_order'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('sc_users.id'))
    car_id = db.Column(db.Integer, db.ForeignKey('sc_cars.id'))
    order_time = db.Column(db.DateTime, default=datetime.now)
    # 原价
    car_price = db.Column(db.Float)
    # 手续费
    service_charge = db.Column(db.Float)
    #
    # # 成交额
    # turnover = db.Column(db.DECIMAL(), nullable=False)
    # # 订单号
    # serial_number = db.Column(db.String(30), nullable=False)

# class BasicParameters(db.Model):
#     __tablename__ = 'Basic_parameters'
#     id = db.Column(db.Integer, primary_key=True)
#     certificate=db.Column(db.String(20))#证件品牌型号
#     manufacturer = db.Column(db.String(20))#厂商
#     level=db.Column(db.Integer)#级别
#     engine = db.Column(db.String(20))#发动机
#     gearbox = db.Column(db.String(20))#变速箱
#     body_structure = db.Column(db.String(20))#车身结构
#     size=db.Column(db.String(20))#长*宽*高(mm)
#     wheel_base=db.Column(db.Integer)#轴距(mm)
#     luggage_compartment=db.Column(db.Integer)#行李箱容积(L)
#     curb_weight=db.Column(db.Integer)#整备质量(kg)


#     def __repr__(self):
#         return self.certificate
#
# class Engine(db.Model):
#     __tablename__ = 'sc_engine'
#
#     displacement = db.Column(db.Float)
#     # 进气形式
#     intake_form = db.Column(db.String(50))
#     # 气缸
#     cylinder = db.Column(db.String(50))
#     # 最大马力
#     max_horsepower = db.Column(db.Integer)
#     # 最大扭矩
#     max_torque = db.Column(db.Integer)
#     # 燃油类型
#     car_fuel = db.Column(db.String(10))
#     # 燃油编号
#     fuel_num = db.Column(db.Integer)
#     # 供油方式
#     fuel_method = db.Column(db.String(10))
#     # 排放标准
#     emission_standard = db.Column(db.String(10))
#
# class Chassis_Brake(db.Model):
#     __tablename__ = 'chassis_brake'
#     id = db.Column(db.Integer,primary_key=True)
#     driving_mode = db.Column(db.String(15))#驱动方式
#     help_type = db.Column(db.String(15))#助力类型
#     front_suspension_type = db.Column(db.String(15))#前悬挂类型
#     rear_suspension_type = db.Column(db.String(15))#后悬挂类型
#     front_brake_type = db.Column(db.String(15))#前制动类型
#     rear_brake_type = db.Column(db.String(15))#后制动类型
#     parking_brake_type = db.Column(db.String(15))#驻车制动类型
#     front_tire_specification = db.Column(db.String(20))#前轮胎规格
#     rear_tire_specification = db.Column(db.String(20))#后轮胎规格

# class outsideproperties(BaseModel,db.Model):
#     __tablename__='engineparameter'
#     power_sunroof=db.Column(db.String(10))
#     panoramic_sunroof=db.Column(db.String(10))
#     Electric_suction_door=db.Column(db.String(10))
#     Induction_trunk=db.Column(db.String(10))
#     Rain_sensing_Wipers=db.Column(db.String(10))
#     rear_wiper=db.Column(db.String(10))
#     POWER_WINDOWS=db.Column(db.String(10))
#     ELECTRIC_ADJUSTING_KNOB_EXTERIOR_REAR_VISION_MIRROR=db.Column(db.String(10))
#     Rearview_mirror_heated=db.Column(db.String(10))

# class Students(db.Model):
#     __tablename__ = 'stu'
#
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(20), nullable=True, unique=True)
#     teacher_id = db.Column(db.Integer, db.ForeignKey('tea.id'))
#
# class Teacher(db.Model):
#     __tablename__ = 'tea'
#
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(20), nullable=True, unique=True)
#     students = db.relationship('Students', backref='teacher')
