from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.views.generic import View
from django.http import HttpResponse

from .forms import LoginForm,RegistForm,ForgetForm,ResetPasswordForm
from apps.utils import restful

# 邮箱验证相关
from django.contrib.auth.backends import ModelBackend
from .models import UserProfile,EmailVerifyRecord
from django.db.models import Q
from ..utils.email_send import send_regist_email

#极验
from ..utils.geetest_sdk.geetest import GeetestLib
# config
pc_geetest_id = "b45aeae15e0e01da9eee11e846a7c9c7"
pc_geetest_key = "dbaae76fd8cf385110dc80a18398600a"
def pcgetcaptcha(request):
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)

# Create your views here.
#
# def user_login(request):
#     if request.method == "POST":
#         username = request.POST.get('username', None)
#         password = request.POST.get('password', None)
#         user = authenticate(request, username=username, password=password)
#         if user:
#             login(request, user)
#             return render(request, 'index.html')
#         else:
#             return render(request,'login.html',{"message":'用户名或者密码错误'})
#     else:
#         return render(request,'login.html')

# 重写authenticate 方法,增加邮箱登录
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 登录类视图
class LoginView(View):
    def get(self,request):
        return render(request, 'auth/login.html')
    def post(self,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print("username:",username)
            print("password:",password)
            user = authenticate(request,username=username,password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return restful.ok()
                else:
                    print("user")
                    return restful.params_error('该用户暂未激活,请前往注册邮箱激活')
            else:
                return restful.params_error('用户名或密码错误')
        else:
            print(form.errors)
            return render(request, 'auth/login.html', {'login_form':form})


# 注册类视图
class RegistView(View):
    def get(self,request):
        regist_form = RegistForm()
        context = {
            'regist_form':regist_form
        }
        return render(request,'auth/register.html',context=context)

    def post(self,request):
        regist_form = RegistForm(request.POST)
        if regist_form.is_valid():
            username = regist_form.cleaned_data.get('email')
            if UserProfile.objects.filter(email=username):
                return render(request,'auth/register.html',{'regist_form':regist_form,'msg':'用户已经存在'})
            password = regist_form.cleaned_data.get('password')
            # captcha = regist_form.cleaned_data.get('captcha')
            # print("captcha:",captcha)
            user = UserProfile()
            user.username = username
            user.email = username
            user.is_active = False
            user.set_password(password)
            user.save()
            # 此处是以邮箱注册,用户名就是邮箱
            send_regist_email(username,'register')
            return render(request, 'auth/login.html', {'msg': '注册成功,请前往邮箱激活!'})
        else:
            print(regist_form.errors)
            return render(request,'auth/register.html',{'regist_form':regist_form,'msg':regist_form.errors})

# 激活类试图
class ActiveView(View):
    def get(self,request,active_code):
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        if all_record:
            for record in all_record:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request,'auth/active_fail.html')

        return render(request, 'auth/login.html')

# 忘记密码
class ForgetView(View):
    def get(self,request):
        forget_form = ForgetForm()
        return render(request,'auth/forgetpwd.html',{'forget_form':forget_form})
    def post(self,request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = forget_form.cleaned_data.get('email')
            send_regist_email(email,'forget')
            return render(request,'auth/send_success.html')
        else:
            render(request,'auth/forgetpwd.html',{'forget_form':forget_form})

# 重置密码
# 忘记密码--邮箱--点击链接--跳转到重置密码界面--输入新密码--更新密码--修改成功,跳转到登录界面
class ResetPasswordView(View):
    def get(self,request,active_code):
        # print("active_code",active_code)
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        # for record in all_records:
        #     print("record",record)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request,'auth/password_reset.html',{'email':email})
        else:
            return render(request, 'auth/login.html')

# 参数冲突,重新定义修改密码视图
class ModifyPwdView(View):
    def post(self,request):
        modify_form = ResetPasswordForm(request.POST)
        if modify_form.is_valid():
            pwd1 = modify_form.cleaned_data.get('password1')
            pwd2 = modify_form.cleaned_data.get('password2')

            email = request.POST.get('email')

            if pwd1 != pwd2:
                return render(request, 'auth/password_reset.html', {'msg': '两次密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.set_password(pwd2)
            user.save()

            return render(request, 'auth/login.html', {'msg': '密码修改成功!'})
        else:
            email = request.POST.get('email')
            print(modify_form.errors)
            return render(request,'auth/password_reset.html',{'email':email,"modify_form":modify_form})


# 登出函数
def my_logout(request):
    logout(request)
    return render(request, 'auth/index.html')