from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from ..organization.models import CourseOrg
# Create your models here.

# 用户扩展
class UserProfile(AbstractUser):
    gender_choice = (
        ("male","男"),
        ("female","女")
    )

    nick_name = models.CharField('昵称',max_length=50,default="")
    birthday = models.DateField("生日",null=True,blank=True)
    gender = models.CharField("性别",max_length=10,choices=gender_choice,default='female')
    address = models.CharField("地址",max_length=100,default="")
    mobile = models.CharField("手机号",max_length=11,null=True,blank=True)
    avatar_img = models.ImageField(upload_to='image/%Y/%m',default='image/2018/11/322767.jpg',max_length=100)

    class Meta:
        verbose_name = "用户信息"
        # 这是干嘛的?
        verbose_name_plural = verbose_name


    def __str__(self):
        return self.username

# 邮箱验证码
class EmailVerifyRecord(models.Model):
    send_choices = (
        ("register","注册"),
        ("forget",'找回密码'),
        ('update_email','修改邮箱')
    )

    code = models.CharField('验证码',max_length=100)
    email = models.EmailField('邮箱',max_length=50)
    send_type = models.CharField('发送类型',choices=send_choices,max_length=30)
    send_time = models.DateTimeField('发送时间',auto_now_add=True)

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name

class Banner(models.Model):
    title = models.CharField('标题',max_length=100)
    # image = models.ImageField("轮播图",upload_to='image/banner/%Y/%m',max_length=100)
    img_url = models.CharField('轮播图',max_length=100,default="")
    link_url = models.URLField("访问地址",max_length=200)
    index = models.IntegerField("优先级",default=0)
    add_time = models.DateTimeField('添加时间',auto_now_add=True)

    class Meta:
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title





