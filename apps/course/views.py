from django.shortcuts import render
from django.views.generic import View
from .models import Course
from pure_pagination import PageNotAnInteger,Paginator
from ..operation.models import UserFavorite,UserCourse,CourseComments

from ..utils import restful
from django.views.decorators.http import require_POST

from ..utils.mixin_utils import LoginRequiredMixin
from  .forms import AddCommentForm

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
        course.click_nums += 1
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

# 开始学习
class CourseInfoView(LoginRequiredMixin,View):
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        user = request.user

        # 课程关联
        # 点击学习后,把课程和用户管理起来
        usercourse = UserCourse.objects.filter(user=user,course=course)
        if not usercourse:
            usercourse = UserCourse(user=user,course=course)
            usercourse.save()
        # 相关课程推荐
        # 先获取所有学习该课程的学员
        users = UserCourse.objects.filter(course=course).all()
        # 获取学员id
        user_ids = [user.user_id for user in users]
        # 获取这些学员所学的所有课程
        all_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程的id
        course_ids = [course.course_id for course in all_courses]
        #　取出相关课程
        related_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums').all()[:3]

        # if user:
        #     user_courses = UserCourse.objects.filter(user=request.user).all()[:3]
        context = {
            'course':course,
            'related_courses':related_courses
        }
        return render(request,'course/course-video.html',context=context)

# 课程评论
class CourseCommentView(LoginRequiredMixin,View):
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        context = {
            'course':course
        }
        return render(request,'course/course-comment.html',context=context)

# 添加评论
class AddCommentsView(LoginRequiredMixin,View):
    def post(self,request):
        form = AddCommentForm(request.POST)
        if form.is_valid():
            course_id = form.cleaned_data.get('course_id')
            comments = form.cleaned_data.get('comments')
            print("comment:",comments)
            # 添加到数据库
            comment = CourseComments(user=request.user,course_id=int(course_id),comments=comments)
            comment.save()
            return restful.ok()
        else:
            print(form.errors)
            return restful.params_error('评论发表失败')