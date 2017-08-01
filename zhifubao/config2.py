class settings:
    # 安全检验码，以数字和字母组成的32位字符
    ALIPAY_KEY = 'o0f7yua35rrxa9jj881h63i92f0pvx20'

    ALIPAY_INPUT_CHARSET = 'utf-8'

    # 合作身份者ID，以2088开头的16位纯数字
    ALIPAY_PARTNER = '2088721367731375'

    # 签约支付宝账号或卖家支付宝帐户
    ALIPAY_SELLER_EMAIL = '470235676@qq.com'

    ALIPAY_SIGN_TYPE = 'RSA2'

    # 付完款后跳转的页面（同步通知） 要用 http://格式的完整路径，不允许加?id=123这类自定义参数
    ALIPAY_RETURN_URL = 'http://relalive.com/zhifubao/zfb/'

    # 交易过程中服务器异步通知的页面 要用 http://格式的完整路径，不允许加?id=123这类自定义参数
    ALIPAY_NOTIFY_URL = 'http://relalive.com/zhifubao/zfb/'