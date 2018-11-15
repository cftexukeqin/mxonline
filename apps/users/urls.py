from django.urls import path,re_path
from . import views
app_name = 'auth'

urlpatterns = [
    path('login/',views.LoginView.as_view(),name='login'),
    path('logout/',views.my_logout,name='logout'),
    path('regist/',views.RegistView.as_view(),name='regist'),
    path('modifypwd/',views.ModifyPwdView.as_view(),name='modifypwd'),
    # 忘记密码
    path('forget/', views.ForgetView.as_view(), name='forget'),
    # 发送激活邮件
    re_path(r'active/(?P<active_code>.*)/',views.ActiveView.as_view(),name='active'),
    # 重置密码
    re_path(r'reset/(?P<active_code>.*)/',views.ResetPasswordView.as_view(),name='reset_pwd'),
    # 极验验证码
    path('pc-geetest/login/', views.pcgetcaptcha, name='pcgetcaptcha'),



]