from django.db import models

from datetime import datetime

# 城市信息
class CityDict(models.Model):
    name = models.CharField('城市',max_length=20)
    desc = models.CharField('描述',max_length=200)
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = '城市'
        verbose_name_plural= verbose_name

# 课程机构基本信息
class CourseOrg(models.Model):
    ORG_CHOICES = (
        ('pxjg','培训机构'),
        ('gx','高校'),
        ('gr','个人'),
    )
    name = models.CharField('机构名称',max_length=50)
    desc = models.TextField('机构描述')
    click_nums = models.IntegerField('点击数',default=0)
    fav_nums = models.IntegerField('收藏数',default=0)
    image = models.ImageField('封面图',upload_to='org/%Y/%m',max_length=100)
    students = models.IntegerField('学习人数',default=0)
    course_nums = models.IntegerField('课程数',default=0)
    address = models.CharField('机构地址',max_length=150,)
    city = models.ForeignKey(CityDict,verbose_name='所在城市',on_delete=models.CASCADE)
    add_time = models.DateTimeField('添加日期',auto_now_add=True)
    category = models.CharField(choices=ORG_CHOICES,max_length=20,verbose_name='机构类别',default='pxjg')

    class Meta:
        verbose_name = '课程机构'
        verbose_name_plural = verbose_name

    # 获取教师数量
    def get_teacher_nums(self):
        return self.teacher_set.all().count()

    def __str__(self):
        return self.name

class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg,verbose_name='所属机构',on_delete=models.CASCADE)
    name = models.CharField('教师名',max_length=50)
    work_years = models.IntegerField('工作年限',default=0)
    work_company = models.CharField('就职公司',max_length=50)
    work_position = models.CharField('公司职位',max_length=50)
    points = models.CharField('教学特点',max_length=50)
    click_nums = models.IntegerField('点击数',default=0)
    fav_nums = models.IntegerField('收藏数',default=0)
    add_time = models.DateTimeField('添加日期',auto_now_add=True)
    age = models.IntegerField('教师年龄',default="",blank=True)
    image = models.ImageField(upload_to='teacher/%Y/%m',default="",verbose_name="头像",max_length=100)

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "[{0}]的教师: {1}".format(self.org, self.name)
