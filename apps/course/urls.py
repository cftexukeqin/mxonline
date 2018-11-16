from django.urls import path,re_path
from . import views
app_name = 'course'

urlpatterns = [
    # 课程主页
    path('',views.CourseIndexView.as_view(),name='index'),
    # 课程详情
    path('<course_id>/',views.CourseDetailView.as_view(),name='detail'),

]