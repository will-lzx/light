import base64

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


# 签名函数
def sign(data, private_key_file_name='/root/zhifubao/app_private_key'):
    """
    签名函数使用指定的公钥Key对文件进行签名，并将签名结果写入文件中
    :param data: 待签名的数据文件
    :param private_key_file_name: 用于签名的私钥文件
    :return: 签名数据
    """
    # 从PEM文件中读取私钥数据
    #key_data = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAhug73b3e2juIOIfxN7Ju2AMcwdOVqG4txOCea+r6nQBMyrlEIIbi1gKWFIbTCJAeKRhJPAZnApd8CCPGwSgRyxbYAUxJNF4BTIECTIHc0nXZVJASv6L0Miqnv7G2X1PFSWMlt4ijmo0f3mCnZONbk8MKcesSSN0EV5WfyJA/PUs+4rbJrEwCnoEtR6TgX+JPg+oa03/718T3jJGz4saWRH7QJD+jPFluZusy2LEMmckX+ZPusSpGZdEunqxbCoM8ywN+Ag2h9L6qOdj1VMTlzu/vweRyZDBW2ztWelbuzW7JRPrIGce0X0vomJ1ATEIPuCidaP16V6K+sguWsgNe8wIDAQAB'

    key_file = open(private_key_file_name, 'rb')
    key_data = key_file.read()
    key_file.close()

    # 从PEM文件数据中加载公钥
    private_key = serialization.load_pem_private_key(
        key_data,
        password=None,
        backend=default_backend()
    )

    # 使用私钥对数据进行签名
    # 指定填充方式为PKCS1v15
    #
    signature = private_key.sign(
        data,
        padding.PKCS1v15(),
        hashes.SHA256()
    )

    # 返回签名数据
    return base64.b64encode(signature)


if __name__ == '__main__':
    # 指定数据文件
    data_file = r'data.bin'
    # 指定签名结果文件
    signature_file = r'signature.bin'
    # 指定签名的私钥
    private_key_file = r'Key.pem'

    # 签名并返回签名结果
    signature = sign(data, private_key_file)
    # 打印签名数据
    [print('%02x' % x, end='') for x in signature]