from django.shortcuts import render
from django.views.generic import View
from pure_pagination import PageNotAnInteger,Paginator
from django.http import HttpResponse

from .models import CourseOrg,CityDict
from .forms import AskForm
from ..utils import restful
from ..operation.models import UserFavorite

# Create your views here.
class IndexView(View):
    def get(self,request):
        # 所有机构
        all_orgs = CourseOrg.objects.all()
        hot_orgs = all_orgs.order_by("-click_nums")[:3]
        # 所有城市
        cities = CityDict.objects.all()
        # 获取城市ID
        # 前端通过href='?city={{city.id}}'的方式进行传参,后端通get方式进行获取
        city_id = request.GET.get('city',"")

        # 类别
        category = request.GET.get('ct',"")
        if category:
            all_orgs = all_orgs.filter(category=category)


        # 机构数量
        org_count = all_orgs.count()


        # 学习人数和课程数筛选
        sort = request.GET.get('sort',"")
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            if sort == "course_nums":
                all_orgs = all_orgs.order_by("-course_nums")

        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))
        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs,2,request=request)
        orgs = p.page(page)
        context = {
            'orgs':orgs,
            'cities':cities,
            'org_count':org_count,
            'city_id':city_id,
            'category':category,
            'hot_orgs':hot_orgs,
            'sort':sort
        }
        return render(request,'organization/index.html',context=context)

class UserAskView(View):
    def post(self,request):
        askform = AskForm(request.POST)
        if askform.is_valid():
            # username = askform.cleaned_data.get('name')
            # mobile = askform.cleaned_data.get('mobile')
            # course_name = askform.cleaned_data.get('course_name')
            user_ask = askform.save(commit=True)
            return restful.ok()
        else:
            return restful.params_error("验证失败")
#机构首页
def orgdetailindex(request,org_id):
    if request.method == "GET":
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()[:4]
        all_teachers = course_org.teacher_set.all()[:2]
        org_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user,fav_id=course_org.id,fav_type=2):
                org_fav = True
        context = {
            'course_org':course_org,
            'all_courses':all_courses,
            'all_teachers':all_teachers,
            'current_page':'home',
            # 机构是否收藏
            'org_fav':org_fav
        }
        return render(request,'organization/org-detail-homepage.html',context=context)
#机构课程
class OrgHomeCourseView(View):
    def get(self,request,org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()
        context = {
            'course_org':course_org,
            'all_courses':all_courses,
            'current_page':'course'
        }
        return render(request,'organization/org-detail-course.html',context=context)

# 机构简介
class OrgHomeDescView(View):
    def get(self,request,org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        context = {
            'course_org':course_org,
            'current_page':'desc'
        }
        return render(request,'organization/org-detail-desc.html',context=context)

# 机构教师
class OrgHomeTeachView(View):
    def get(self,request,org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()
        context = {
            'course_org':course_org,
            'all_teachers':all_teachers,
            'current_page':'teach'
        }
        return render(request,'organization/org-detail-teachers.html',context=context)

# 机构收藏
# class AddFavView(View):
#     def post(self,request):
#         fav_id = request.POST.get('fav_id',0)
#         fav_type = request.POST.get('fav_type',0)
#
#         if not request.user.is_authenticated:
#             return restful.noauth(message='请先登录')
#         exists = UserFavorite.objects.filter(fav_id=int(fav_id),fav_type=int(fav_type),user=request.user)
#
#         if exists:
#             # 如果已经收藏,点击之后取消收藏
#             exists.delete()
#             return restful.ok()
#         else:
#             user_fav = UserFavorite()
#             user_fav.user = request.user
#             user_fav.fav_id = fav_id
#             user_fav.fav_type = fav_type
#             user_fav.save()
#             return restful.ok()
class AddFavView(View):
    """
    用户收藏和取消收藏
    """
    def post(self, request):
        id = request.POST.get('fav_id', 0)         # 防止后边int(fav_id)时出错
        type = request.POST.get('fav_type', 0)     # 防止int(fav_type)出错

        if not request.user.is_authenticated:
            return restful.noauth(message='用户未登录')

        exist_record = UserFavorite.objects.filter(user=request.user, fav_id=int(id), fav_type=int(type))
        if exist_record:
            exist_record.delete()
            return restful.ok(message="收藏")
        else:
            user_fav = UserFavorite()
            if int(id) > 0 and int(type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(id)
                user_fav.fav_type = int(type)
                user_fav.save()
                return restful.ok(message="已收藏")
            else:
                return restful.params_error(message="收藏出错!")


