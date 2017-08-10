"""
Django settings for l project.

Generated by 'django-admin startproject' using Django 1.11.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vlpxdbqk6mh7ijj+^0het=6l+k&sqi=wumtpw-!9=6h^j#c%a^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

SESSION_SAVE_EVERY_REQUEST = True

# Application definition

INSTALLED_APPS = [
    'home',
    'weixin',
    'wechat',
    'wechat_pay',
    #'zhifubao',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'light.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'light.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'light',
        'USER': 'root',
        'PASSWORD': 'Password01?',
        'HOST': '106.14.151.3',
        'PORT': '3306',
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_ROOT = '/var/www/alglab/static'
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    '/var/www/static/',
]

# weixin
WECHAT_TOKEN = "relalive"
WEIXIN_APPID = 'wxe2d133d468969a91'
WEIXIN_APPSECRET = '4fa59c6b06441dec0238fbf0df841c63'
WEIXIN_DEPOSIT = 0.01
WEIXIN_PAYBACK = 'http://relalive.com/weixin/payback/'
WEIXIN_RETURNPAYBACK = 'http://relalive.com/weixin/returnpayback/'
WEIXIN_IP = '106.14.151.3'


APPEND_SLASH = False

tmp_pwd = 'Password'
tmp_mail = 'tmp_mail@relalive.com'

WECHAT = [
    {
        'appid': 'wxe2d133d468969a91',
        'appsecret': '4fa59c6b06441dec0238fbf0df841c63',
        'token': 'relalive',
        'mch_id': '1486517162',
        'key': 'qingpaikeji201700000000000000000',
        'body': '押金支付',
    },
]

ALIPAY_PARTNERID = '2088721367731375'
ALIPAY_ACCOUNT = '470235676@qq.com'


CABINET_CAPACITY = '50'
