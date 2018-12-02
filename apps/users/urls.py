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
    #　个人中心
    re_path('usercenter/(?P<user_id>.*)/',views.UserProfileView.as_view(),name='usercenter'),
    # 个人中心-我的课程
    re_path('usercourse/(?P<user_id>.*)/',views.usercourse,name='usercourse'),
    # 个人中心-我的收藏
    re_path('userfav/(?P<user_id>.*)/',views.userfav,name='userfav'),
    # 个人中心-我的消息
    re_path('usermsg/(?P<user_id>.*)/',views.usermessage,name='usermsg'),
    # 更换头像
    path('avatar/upload/',views.UploadAvatarView.as_view(),name='avatar_upload'),
    # 更改密码
    path('pwdreset/',views.UserCenterResetPwdView.as_view(),name='usercenter_pwdreset')

]