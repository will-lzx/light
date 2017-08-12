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
    key_data = "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCUkAy5322rUVugNE4oyzK8kOkvMjJfVwltHL5jH7wLvSxDtIxfxlve3490Q/mXBy/EXfVKyd25ZkWP4WTH4dDB5fC5+CC/jP2aDt/Ex6RfF1eutladOT1MC6Y91H+ZXKdXh9LX/ZnMjh8r5yszXG0NvKZOmuVSj7cO6xRrNG9xZxN1Lg5Vh3OUBxW/Ux6sPjJhe0bzpYqCoHQRS1+dP11nRtVczFzuBQXcfdi48lLC+KjP4IBrG34QvZYsgNPCk5VwFae00TWfiU7YSG9I1nrw/gVd7LCTA+9QZIcYMi53SLh76Q3ryMNiPYsIwC/HsV2q3p0KzVzvrf3TNPgPfqilAgMBAAECggEAYiJhdaqkTAV7C/FhK8tGIY9rqVR0N8xLmrrg/KNq2SpGAhdSnrVt3GQ646c/SMdjg0g5jwSXpS9sheVyaCK/fkXA5WeFYmLk5o4qvFbQOkw2DF/ACS1VU1Vio/cpromotMYwvaJ0pM3Aw4R5Yf0MwIU8KjJhh08NshoRK9vAPdy9iJnTUVPTyyLl76p8rXHYePppZEUQUF3pr27NCwtTTgOyssZh8kH0Rm2ImWfNQ0nD7oTe6Be0wLJ5SN5wze0QKWssNFy0q0oHTemDoKvqVBp2WnRQBnNpEcb1Ahj7o1b68JBuyH/+1bXC3xquVPFPWO5oYlpunWS02AJ4/bKb4QKBgQDr4Eu6ljyzl3onvqUIIfbZJzCCat63gMfJHyzogDxVSWm6n6dbQwHVoc5wu26gKB3lFRq7eU6PNvC0TUmOfEVKTuT6o91dLI5QojEwwBNk9eO2XpktNm6Hp4Ejf06Y/fR3soLTKFNFuvy79setJds5SHxAq7HmwxJNRD8xDN8YeQKBgQChPMPusOjaDCJi5A/vqlgntZgwycNTcHZeK04nk/0ZMttC2l/V2fE85MT/AkK16nksXF7/Ih8sK8uOzCiNzRkmCx59Ci6gDWsb36SSsA3I6Rdxmn3hW47Zh0ObvstdJvNpliCaMIc9t/kRsrOUjuFJjI37jTvBWOj0I6V/AcAejQKBgQCAAMd36UHlwAVVfjr279+Stpa3n6Ffee5xcY6gWb7kFaPf1/YtK27abSWnvb9qAHtArzRDmrAMPidf4TVSspOzoJ7YeYaOorhUf8AsEYA04M+DT1DW3VwcF8WX6uVPVzmMn34pcw/FnpS6uFBh4VJXgsOTINm5PhE3hxq31qFXGQKBgBFf0OUpnw3P/OyXEriKrJEq2kl3lFqrZbXkCLnvEnjiqAneKjGLGJmtNSUdgz7DE2eaVIo9jQpfdcHfcgdFsI4O6Kwkqr2IdKA+SyebXQDnTSVqtmHQUeZS0xA3UQaqqdQY305+KDSYXHhxvzQk6VXZlXsjzuqYwBF+vdifwaoJAoGAbX11wE0h9kjU1RocZ6MfMtZ2AZRdP8LfrQSzh8mLxlR++2iB0ttX79wcVKrmfgKwc2FRPXrNWKI109pjtM8XVBScg8O+p1uZOXlePedViEnrf62NFA6a2/9FvOFWDRm7z6YgcCYk6NvUI3f9bPO3yYfhCvwLDhCG476hhOPU6qI=";

    # key_file = open(private_key_file_name, 'rb')
    # key_data = key_file.read()
    # key_file.close()

    # 从PEM文件数据中加载公钥
    # private_key = serialization.load_pem_private_key(
    #     key_data,
    #     password=None,
    #     backend=default_backend()
    # )
    private_key = serialization.load_der_private_key(
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