import xadmin

from .models import EmailVerifyRecord,Banner
from xadmin import views

# xadmin 主题配置
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

# 将基本配置管理与view绑定
xadmin.site.register(views.BaseAdminView,BaseSetting)

# xadmin中这里是继承object,不是继承admin
class EmailVerifyRecordAdmin(object):
    # 显示的列
    list_display = ['code','email','send_type','send_time']
    # 搜索的字段,不要添加时间搜索
    search_fields = ['code','email','send_type']
    # 过滤
    list_filter = ['code','email','send_type','send_time']
    pass

xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)


# 显示Banner
class BannerAdmin(object):
    list_display = ['title','image','image_url','index','add_time']
    search_fields = ['title','image','image_url','index']
    list_filter = ['title','image','image_url','index','add_time']

xadmin.site.register(Banner,BannerAdmin)