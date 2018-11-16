from django.shortcuts import render
from django.views.generic import View
from .models import Course
from pure_pagination import PageNotAnInteger,Paginator
from ..operation.models import UserFavorite
from ..utils import restful
from django.views.decorators.http import require_POST

# Create your views here.
# 课程首页
class CourseIndexView(View):
    def get(self,request):
        all_courses = Course.objects.all()
        hot_courses = Course.objects.order_by('-students').all()[:4]
        # 获取分类参数
        sort = request.GET.get('sort','')
        if sort == 'students':
            # 按照学习人数排序
            all_courses = all_courses.order_by('-students').all()
        elif sort == 'hot':
            # 按照收藏人数排序
            all_courses = all_courses.order_by('-fav_nums').all()
        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1
        # 分页功能
        p = Paginator(all_courses,3,request=request)
        courses = p.page(page)
        context = {
            'courses':courses,
            'sort':sort,
            'hot_courses':hot_courses
        }
        return render(request,'course/course-list.html',context=context)

class CourseDetailView(View):
    def get(self,request,course_id):
        course = Course.objects.select_related('course_org').get(id=int(course_id))
        course.click_unms += 1
        course.save()
        tag = course.tag
        related_courses = None
        fav_course = False
        fav_org = False
        # 判断课程是否收藏
        if UserFavorite.objects.filter(user=request.user,fav_id=course.id,fav_type=1):
            fav_course = True
        # 判断机构是否收藏
        if UserFavorite.objects.filter(user=request.user,fav_id=course.course_org.id,fav_type=2):
            fav_org = True
        if tag:
            # 相关课程
            related_courses = Course.objects.filter(tag=tag).all()[1:3]
        context = {
            'course':course,
            'related_courses':related_courses,
            'fav_course':fav_course,
            'fav_org':fav_org
        }
        return render(request,'course/course-detail.html',context=context)
class CourseLessonView(View):
    def get(self,request):
        return render(request,'course/course-video.html')

class CourseCommentView(View):
    def get(self,request):
        return render(request,'course/course-comment.html')