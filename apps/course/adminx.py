import xadmin
from .models import Course,Lesson,Video,CourseResource


#  目前在添加课程的时候没法添加章节和课程资源，我们可以用inlines去实现这一功能
class LessonInline(object):
    model = Lesson
    extra = 0

class CourseResourseInline(object):
    model = CourseResource
    extra = 0


class CourseAdmin(object):
    "课程"
    list_display = [ 'name','desc','detail','degree','learn_times','students']
    search_fields = ['name','desc','detail','degree','students']
    list_filter = ['name','desc','detail','degree','learn_times','students']
    model_icon = 'fa fa-book'
    # 按照点击数排序
    ordering = ['-click_nums']
    # 只读字段,不能编辑
    readonly_fields = ['click_nums']
    # 不显示的字段
    exclude = ['fav_nums']

    # 在CourseAdmin中使用inline 添加项目两个类
    inlines = [LessonInline,CourseResourseInline]

    # 列表页可编辑相关内容
    list_editable = ['degree','desc']

    #detail就是要显示为富文本的字段名
    style_fields = {"detail": "ueditor"}

class LessonAdmin(object):
    '章节'
    list_display = ['course','name','add_time']
    search_fields = ['course','name']
    list_filter = ['course','name','add_time']

class VideoAdmin(object):
    '视频'
    list_dispaly = ['lesson','name','add_time']
    search_fields = ['lesson','name']
    list_filter = ['lesson','name','add_time']

class CourseResourceAdmin(object):
    '课程资源'
    list_display = ['course','name','add_time']
    search_fields = ['course','name']
    list_filter = ['course','name','add_time']

#　注册
xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(CourseResource,CourseResourceAdmin)
