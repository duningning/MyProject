import datetime

from django.shortcuts import render
from Myapp.models import *

# Create your views here.

def home(request):

    res = {}
    res['username'] = request.user.username

    res['href'] = DB_href.objects.all() # 从数据库中拿超链接数据
    res['platform'] = DB_platform.objects.all() # 平台数据

    return render(request,'home.html',res)# 后端用来把前端的home.html文件返回给浏览器