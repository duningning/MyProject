import datetime
import os
import shutil

from django.shortcuts import render
from Myapp.models import *
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.

def home(request):

    res = {}
    res['username'] = request.user.username

    res['href'] = DB_href.objects.all() # 从数据库中拿超链接数据
    res['platform'] = DB_platform.objects.all() # 平台数据

    return render(request,'home.html',res)# 后端用来把前端的home.html文件返回给浏览器

# 新增端
def save_platform(request):
    # 取到用户前端输入的值
    platform_name = request.GET["platform_name"]
    platform_host = request.GET["platform_host"]

    # 数据更新到数据库
    platform = DB_platform.objects.create(name=platform_name,host=platform_host)
    # 复制出自己的调试包
    new_client_name = 'client_'+str(platform.id)
    demo_path = 'MyClient/demo_client'
    new_path = 'MyClient/'+new_client_name
    shutil.copytree(demo_path,new_path)


    return HttpResponse('')

def del_platform(request,did):
    # 取到用户前端输入的值
    DB_platform.objects.filter(id=did).delete() # 删除数据库指定数据

    return HttpResponse('')

# 进入用例列表页
def case_list(request,did):
    cases = DB_case.objects.filter(platform_id=did)

    res = {}
    res['cases']= cases
    res['platform'] = DB_platform.objects.filter(id =did)[0]
    res['href'] = DB_href.objects.all() # 从数据库中拿超链接数据
    return render(request,'case.html',res)

#添加用例
def add_case(request, did):
    DB_case.objects.create(platform_id=did)
    return HttpResponseRedirect('/case_list/'+did+'/')
    #return case_list(request,did)

#删除用例
def del_case(request, cid):
    case = DB_case.objects.filter(id = cid)
    palatform_id = case[0].platform_id
    case.delete()
    return HttpResponseRedirect('/case_list/'+palatform_id+'/')