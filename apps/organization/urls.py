from django.urls import path,re_path
from . import views
app_name = 'org'


urlpatterns = [
    path('',views.IndexView.as_view(),name='index'),
    path('ask/',views.UserAskView.as_view(),name='ask'),
    #机构主页
    re_path('home/(?P<org_id>\d+)/',views.orgdetailindex,name='org_home'),
    # 机构课程
    re_path('course/(?P<org_id>\d+)/',views.OrgHomeCourseView.as_view(),name='org_course'),
    # 机构简介
    re_path('desc/(?P<org_id>\d+)/',views.OrgHomeDescView.as_view(),name='org_desc'),
    # 机构老师
    re_path('teacher/(?P<org_id>\d+)/',views.OrgHomeTeachView.as_view(),name='org_teach'),
    # 机构收藏
    path('addfav/',views.AddFavView.as_view(),name='addfav'),
]

