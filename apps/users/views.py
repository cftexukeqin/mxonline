from django.shortcuts import render
from django.contrib.auth import authenticate,login
# Create your views here.

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return render(request, 'index.html')
        else:
            return render(request, 'login.html', {'message': '请重新登录'})
    else:
        return render(request,'login.html')
