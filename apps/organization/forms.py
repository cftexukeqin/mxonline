from django import forms

from ..operation.models import UserAsk

# 咨询
class AskForm(forms.ModelForm):
    "我要咨询"
    class Meta:
        model = UserAsk
        fields = ['name','mobile','course_name']

    # def clean_mobile(self):
    #     "验证手机号"
    #     mobile = self.cleaned_data.get('mobile')
    #     d