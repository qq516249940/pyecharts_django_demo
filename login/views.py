from django.shortcuts import render,HttpResponse
from login import models
# Create your views here.

user_list = []

def index(request):
    # return HttpResponse("hello world welcome login")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        # temp = {'user': username, 'pwd': password}
        # user_list.append(temp)
        # 将数据保存到数据库
        models.UserInfo.objects.create(user=username, pwd=password)
    # 从数据库中读取所有数据，注意缩进
    user_list = models.UserInfo.objects.all()
    return render(request, 'index.html',{'data': user_list})    
