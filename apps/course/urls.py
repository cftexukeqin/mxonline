from django.urls import path,re_path
from . import views
app_name = 'course'

urlpatterns = [
    # 课程主页
    path('',views.CourseIndexView.as_view(),name='index'),
    # 课程详情
    path('<int:course_id>/',views.CourseDetailView.as_view(),name='detail'),
    # 课程章节
    re_path(r'info/(?P<course_id>\d)/',views.CourseInfoView.as_view(),name='info'),
    # 课程评论
    re_path(r'comment/(?P<course_id>\d)/',views.CourseCommentView.as_view(),name='comment'),
    # 发表评论
    path('addcomment/',views.AddCommentsView.as_view(),name='addcomment')

]