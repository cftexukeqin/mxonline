from django import forms

from captcha.fields import CaptchaField
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