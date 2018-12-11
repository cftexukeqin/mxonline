"""mxonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path,include,re_path
import xadmin
from django.views.generic import TemplateView

from django.views.static import serve
from mxonline.settings import MEDIA_ROOT
from apps.users import views


urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('', views.IndexView.as_view(), name='index'),
    # 用户相关路由
    path('user/',include('apps.users.urls')),
    path('captcha/',include('captcha.urls')),
    path('org/',include('apps.organization.urls')),
    path('course/',include('apps.course.urls')),
    # 处理图片显示的url
    re_path(r'^media/(?P<path>.*)',serve,{'document_root':MEDIA_ROOT}),
    # Ueditor
    path('ueditor',include('DjangoUeditor.urls')),
    # haystack 配置
    path('search/',include('haystack.urls'))

]
