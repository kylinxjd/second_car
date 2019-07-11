import redis


class Config(object):
    """
    项目配置
    """
    SECRET_KEY = 'saddfs1f2sfsd5fs5f31d21d21x2cz'

    # DEBUG = True

    # todo mysql数据库的配置
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1:3306/cars'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # todo redis配置
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    # todo 配置session
    SESSION_TYPE = 'redis'
    # 创建redis链接
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST,
                                      port=REDIS_PORT)
    # 签名,将cookie中的session——id加密
    SESSION_USE_SIGNER = True
    # 生命周期
    PERMANENT_SESSION_LIFETIME = 3600


class DevelopmentConfig(Config):
    # 调试模式
    DEBUG = True


class OnlineConfig(Config):
    # 上线模式
    DEBUG = False


config = {
    'dev': DevelopmentConfig,
    'online': OnlineConfig
}
