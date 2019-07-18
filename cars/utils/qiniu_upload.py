from qiniu import Auth, put_data

access_key = 'driOIprRvi96vor7cDN9QNI42oK2jkAhgezx1D_e'

secret_key = '-jP_bKXyMt2Ph1I_d4w8_ixj8lw6M7W0UWxvznMm'

# 空间名
bucket_name = 'cars'


def qiniu_upload_file(data):
    """
    上传文件
    :param data: 要上传的bytes类型数据
    :return:
    """
    # 创建鉴权对象
    q = Auth(access_key=access_key, secret_key=secret_key)

    # 生产token, 上传凭证
    token = q.upload_token(bucket=bucket_name)

    # 上传文件
    ret, res = put_data(token, 'myjxjd', data=data)
    ret.get('key')

    print(ret)

    print(res)

    if res.status_code != 200:
        raise Exception("upload failed")

    return ret, res

