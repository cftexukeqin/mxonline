"""
Django settings for mxonline project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import sys
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,os.path.join(BASE_DIR,'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ih5rc1#21im0!-d($8^86gg((9q!)q9gvfx0y!o9q((ldsa45o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["118.126.108.129"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 注册app
    "apps.users",
    "apps.course",
    'apps.operation',
    'apps.organization',
    # xadmin配置
    'xadmin',
    'crispy_forms',
    # 验证码配置
    'captcha',
    #分页功能
    'pure_pagination',
    # 序列化数据 传递json格式的数据给前端
    'rest_framework',
    # 集成Ueditor
    "DjangoUeditor",
    # 全局搜索
    'haystack'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mxonline.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'mxonline.wsgi.application'

# 静态文件路径
STATIC_ROOT = os.path.join(BASE_DIR,'static_dist')


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "mxonline",
        "USER":"root",
        "HOST":"127.0.0.1",
        'PASSWORD':'123456',
        "PORT":3306
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

# 设置USER_MODEL
AUTH_USER_MODEL = 'users.UserProfile'

# 配置静态文件
STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'static')
]

# 邮箱登录功能配置
AUTHENTICATION_BACKENDS = (
    'apps.users.views.CustomBackend',
)

# 邮箱配置
EMAIL_HOST = "smtp.qq.com"  # SMTP服务器主机
EMAIL_PORT = 587             # 端口
EMAIL_HOST_USER = "1527507926@qq.com"       # 邮箱地址
EMAIL_HOST_PASSWORD = "zaczojaxmedgbaeh"    # 密码
EMAIL_USE_TLS= True
EMAIL_FROM = "1527507926@qq.com"            # 邮箱地址

# 上传文件路径
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')

# xadmin 源码安装
import os
import sys


sys.path.insert(0,os.path.join(BASE_DIR,'extra_apps'))

# haystack搜索配置
HAYSTACK_CONNECTIONS = {
    'default': {
        # 设置haystack的搜索引擎
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        # 设置索引文件的位置
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    }
}

# 增删改查后自动创建索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'