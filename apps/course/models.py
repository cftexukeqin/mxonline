from django.db import models
# from ..operation.models import UserCourse
from datetime import datetime
from ..organization.models import CourseOrg,Teacher

# 课程模型
class Course(models.Model):
    DEGREE_CHOICES = (
        ('cj',"初级"),
        ('zj','中级'),
        ('gj','高级')
    )

    name = models.CharField('课程名称',max_length=50)
    desc = models.CharField('课程描述',max_length=300)
    detail = models.TextField("课程详情")
    degree = models.CharField('难度',choices=DEGREE_CHOICES,max_length=2)
    learn_times = models.IntegerField("学习时长(分钟数)",default=0)
    students = models.IntegerField("学习人数",default=0)
    fav_nums = models.IntegerField("收藏人数",default=0)
    thumbnail = models.ImageField('封面图',upload_to='images/course/%Y/%m',max_length=100)
    click_nums = models.IntegerField('点击数',default=0)
    add_time = models.DateTimeField('添加时间',auto_now_add=True)
    tag = models.CharField('课程标签',max_length=50,default="")
    teacher = models.ForeignKey(Teacher,verbose_name='课程讲师',on_delete=models.CASCADE,default="",null=True,blank=True)
    notice = models.CharField('课程须知',max_length=300,default="")
    teacher_tell = models.CharField('老师告诉你',max_length=300,default="")
    # 课程所属机构
    course_org = models.ForeignKey(CourseOrg,on_delete=models.CASCADE,verbose_name="所属机构",null=True,blank=True)
    # 课程分类
    category = models.CharField('课程分类',max_length=50,default="")

    # is_banner = models.BooleanField("是否轮播",default=False)

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name
    #获取课程章节数
    def get_lesson_nums(self):
        return self.lesson_set.all().count()

    # 获取课程学习用户
    def get_course_users(self):
        return self.usercourse_set.all()[:4]

    # 返回名称,后台显示
    def __str__(self):
        return self.name

# 章节
class Lesson(models.Model):
    course = models.ForeignKey(Course,verbose_name='课程',on_delete=models.CASCADE)
    name = models.CharField('章节名',max_length=100)
    add_time = models.DateTimeField('添加时间',auto_now_add=True)

    class Meta:
        verbose_name = "章节"
        verbose_name_plural = verbose_name

    def get_video_nums(self):
        return self.video_set.all().count()

    def __str__(self):
        return '<{0}课程的章节> {1}'.format(self.course.name,self.name)

# 视频
class Video(models.Model):
    lesson = models.ForeignKey(Lesson,verbose_name='章节',on_delete=models.CASCADE)
    name = models.CharField('视频名',max_length=100)
    add_time = models.DateTimeField('添加时间',auto_now_add=True)
    url = models.URLField('视频链接',max_length=200,default="")
    learn_time = models.IntegerField('学习时长(分钟)',default=0)

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course,verbose_name='课程',on_delete=models.CASCADE)
    name = models.CharField('名称',max_length=100)
    download = models.FileField('资源文件',upload_to='media/course/resource/%Y/%m')
    add_time = models.DateTimeField('添加时间', auto_now_add=True)

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
