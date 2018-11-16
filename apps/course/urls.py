from django.urls import path,re_path
from . import views
app_name = 'course'

urlpatterns = [
    # 课程主页
    path('',views.CourseIndexView.as_view(),name='index'),
    # 课程详情
    path('<int:course_id>/',views.CourseDetailView.as_view(),name='detail'),
    # 课程章节
    path('lesson/',views.CourseLessonView.as_view(),name='lesson'),
    # 课程评论
    path('comment/',views.CourseCommentView.as_view(),name='comment'),

]