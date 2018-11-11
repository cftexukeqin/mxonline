from django.shortcuts import render
from django.views.generic import View
from pure_pagination import PageNotAnInteger,Paginator

from .models import CourseOrg,CityDict
from .forms import AskForm
from ..utils import restful

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
