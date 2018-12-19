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
    path('info/',views.UserProfileView.as_view(),name='usercenter'),
    # 个人中心-我的课程
    path('course/',views.usercourse,name='usercourse'),
    # 个人中心-我的收藏
    path('fav/',views.userfav,name='userfav'),
    # 个人中心-我的消息
    path('message/',views.usermessage,name='usermsg'),
    # 更换头像
    path('avatar/upload/',views.UploadAvatarView.as_view(),name='avatar_upload'),
    # 更改密码
    path('pwdreset/',views.UserCenterResetPwdView.as_view(),name='usercenter_pwdreset'),
    # 修改邮箱 - 发送邮箱验证码
    path('sendemail/code/',views.SendEmailCodeView.as_view(),name='send_email_code'),
    # 修改邮箱 - 完成邮箱修改
    path('update/email/', views.UpdateEmailView.as_view(), name='update_email'),
    # 个人信息 -保存
    path('update/info/', views.SaveUserInfoView.as_view(), name='save_info'),
    # 注册成功提示
    path('test/',views.test,name='test')

]
