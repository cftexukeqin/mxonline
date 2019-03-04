from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.views.generic import View
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.views.decorators.http import require_POST

from .forms import LoginForm,RegistForm,ForgetForm,ResetPasswordForm,UploadAvatarForm,UpdateUserInfoForm
from apps.utils import restful
from apps.operation.models import UserCourse,UserMessage
# 分页
from pure_pagination import PageNotAnInteger,Paginator

from ..utils.mixin_utils import LoginRequiredMixin

# 邮箱验证相关
from django.contrib.auth.backends import ModelBackend
from .models import UserProfile,EmailVerifyRecord,Banner
from apps.course.models import Course,CourseOrg,Teacher
from django.db.models import Q
from ..utils.email_send import send_regist_email
import json
from datetime import datetime

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


# @method_decorator(cache_page(60*5),name='get')
class IndexView(View):
    def get(self,request):
        # 轮播图
        banners = Banner.objects.all()
        courses = Course.objects.all()[:6]
        orgs = CourseOrg.objects.all()
        teachers = Teacher.objects.all()[:4]

        context = {
            'banners':banners,
            'courses':courses,
            'orgs':orgs,
            "teachers":teachers
        }
        return render(request, 'auth/index.html', context=context)



#极验
from ..utils.geetest_sdk.geetest import GeetestLib
# config geetest 获取后台参数,初始化geetest
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
        # form = LoginForm(request.POST)
        # if form.is_valid():
        #     username = form.cleaned_data.get('username')
        #     password = form.cleaned_data.get('password')
        #     print("username:",username)
        #     print("password:",password)
        #     user = authenticate(request,username=username,password=password)
        #     if user:
        #         if user.is_active:
        #             login(request, user)
        #             return restful.ok()
        #         else:
        #             print("user")
        #             return restful.params_error('该用户暂未激活,请前往注册邮箱激活')
        #     else:
        #         return restful.params_error('用户名或密码错误')
        # else:
        #     print(form.errors)
        #     return render(request, 'auth/login.html', {'login_form':form})
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 获取极验,滑动验证码相关参数
        gt = GeetestLib(pc_geetest_id,pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE,'')
        validate = request.POST.get(gt.FN_VALIDATE,'')
        seccode = request.POST.get(gt.FN_SECCODE,'')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session['user_id']

        if status:
            result = gt.success_validate(challenge,validate,seccode,user_id)
            # print('success result:',result)
        else:
            result = gt.failback_validate(challenge,validate,seccode)
            # print('fail result:',result)

        if result == 1:
            # 验证码正确
            # 利用authenticate()做用户名和密码的校验
            user = authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                return restful.ok()
            else:
                return restful.params_error(message='用户名或密码错误')
        else:
            return restful.noauth(message='请点击验证码进行验证!')


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
            if UserProfile.objects.filter(Q(email=username)|Q(username=username)):
                return render(request,'auth/register.html',{'regist_form':regist_form,'msg':'用户已经存在'})
            else:
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
                send_regist_email(username,code_num=16,send_type='register')
                return render(request, 'auth/regist_to_active.html',)
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
            send_regist_email(email,code_num=16,send_type='forget')
            return render(request,'auth/send_success.html')
        else:
            return render(request,'auth/forgetpwd.html',{'forget_form':forget_form})

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

# 个人中心  主页
class UserProfileView(View):
    def get(self,request):
        unread_msg_count = UserMessage.objects.filter(user=request.user.id,has_read=False).count()
        context = {
            'user':request.user,
            'unread_msg_count':unread_msg_count
        }
        return render(request,'usercenter/usercenter-info.html',context=context)

# 我的课程
def usercourse(request):
    usercourses = UserCourse.objects.filter(user=request.user).all()

    context = {
        'user':request.user,
        'usercourses':usercourses
    }
    return render(request,'usercenter/usercenter-mycourse.html',context=context)

# 我的收藏  机构 课程 老师
def userfav(request):
    user = request.user

    fav_type = request.GET.get('type','org')

    render_template = 'usercenter/usercenter-fav-org.html'
    if fav_type == 'course':
        render_template = render_template
    elif fav_type == 'teacher':
        render_template = 'usercenter/usercenter-fav-teacher.html'
    elif fav_type == 'org':
        render_template = 'usercenter/usercenter-fav-org.html'
    context = {
        'user':user,
        'type':fav_type
    }
    return render(request,template_name=render_template,context=context)


# 个人中心 - 我的消息
def usermessage(request):

    all_messages = UserMessage.objects.filter(user=request.user.id)
    try:
        page = request.GET.get('page',1)
    except PageNotAnInteger:
        page = 1

    p = Paginator(all_messages,4,request=request)
    messages = p.page(page)

    context = {
        'messages':messages
    }
    return render(request,'usercenter/usercenter-message.html',context=context)

# 更换头像
class UploadAvatarView(View,LoginRequiredMixin):
    def post(self,request):
        form = UploadAvatarForm(request.POST,request.FILES)
        if form.is_valid():
            avatar = form.cleaned_data.get('avatar_img')
            print(avatar)
            request.user.avatar_img = avatar
            request.user.save()
            return restful.ok()
        else:
            print(form.get_error())
            return restful.params_error(message=form.get_error())

# 个人中心修改密码

class UserCenterResetPwdView(View):
    def post(self,request):
        pwd1 = request.POST.get('pwd1')
        print(pwd1)
        if pwd1:
            user = request.user
            print(user)
            if user:
                user.set_password(pwd1)
                user.save()
                return restful.ok()
            else:
                return restful.params_error(message='请输入新密码!')

        else:
            return restful.params_error(message='请输入新密码!')

# 发送邮箱验证码
class SendEmailCodeView(LoginRequiredMixin,View):
    def get(self,request):
        email = request.GET.get('email')

        if UserProfile.objects.filter(email=email).first():
            return restful.params_error(message='邮箱已经存在!')

        send_regist_email(email,6,'update_email')
        return restful.ok()

# 完成邮箱修改
class UpdateEmailView(LoginRequiredMixin,View):
    def post(self,request):
        email = request.POST.get('email')

        # user = UserProfile.objects.filter(email=email).first()
        # user.email = email
        # user.save()
        user = request.user
        user.email = email
        user.save()
        return restful.ok()

# 保存个人信息
class SaveUserInfoView(View,LoginRequiredMixin):
    def post(self,request):
        # 实例form 时,传入instance参数,可绑定对象
        # 此列中绑定了request.user 对象
        form = UpdateUserInfoForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            return restful.ok()
        else:
            print(form.get_error())
            return restful.params_error(message=form.get_error())

# 登出函数
def my_logout(request):
    logout(request)
    return render(request, 'auth/index.html')

def test(request):
    return render(request,'auth/regist_to_active.html')