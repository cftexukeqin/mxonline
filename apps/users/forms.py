from django import forms
from .models import UserProfile
from captcha.fields import CaptchaField

from ..forms import FormMixin

# 登錄表單驗證
class LoginForm(forms.Form):

    username = forms.CharField(required=True)
    password = forms.CharField(required=True,min_length=6)

# 注册表单验证
class RegistForm(forms.Form):
    email = forms.CharField(required=True)
    password = forms.CharField(required=True,min_length=6)

    captcha = CaptchaField(error_messages={'invalid':'验证码错误'})

# 忘记密码
class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid':'验证码错误'})

# 重置密码
class ResetPasswordForm(forms.Form):
    password1 = forms.CharField(required=True,min_length=6)
    password2 = forms.CharField(required=True,min_length=6)


# 更换头像
class UploadAvatarForm(forms.ModelForm,FormMixin):

    class Meta:
        model = UserProfile
        fields = ['avatar_img']


# 个人信息修改
class UpdateUserInfoForm(forms.ModelForm,FormMixin):
    class Meta:
        model = UserProfile
        fields = ['nick_name','birthday','address','mobile','gender']