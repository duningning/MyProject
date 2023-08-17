import datetime
import json
import os
import shutil
import subprocess
import threading
import time
import re

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
    platform = DB_platform.objects.create(name=platform_name,host=platform_host,user=request.user.username)
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
    res['hosts'] = DB_platform.objects.filter(id = did)[0].host.split(',')
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

# 用例列表页-设置-获取用例数据
def set_case(request):
    case_id = request.GET['id']
    case = list(DB_case.objects.filter(id=case_id).values())[0]
    print(case)
    print(type(case))

    return HttpResponse(json.dumps(case),content_type="application/json")

# 用例列表页-设置-保存用例数据
def save_case(request):
    case_id = request.GET['case_id']
    case_name = request.GET['case_name']
    case_counts = request.GET['case_counts']
    Concurrency = request.GET['Concurrency']
    monitor = request.GET['monitor']

    DB_case.objects.filter(id=case_id).update(name =case_name,counts=case_counts,Concurrency=Concurrency,monitor=monitor)

    return HttpResponse('')

# 获取监控设置
# def set_monitor(request):
#     # 从前端获取需要的数据
#     platform_id = request.GET["platform_id"]
#     # 跟数据库进行交互
#     monitor = DB_platform.
#     # 返回给前端结果
# # 保存监控设置
def save_monitor(request):
    monitor_time = request.GET['monitor_time']
    monitor_phone = request.GET['monitor_phone']
    monitor_email = request.GET['monitor_email']
    monitor_feishu = request.GET['monitor_feishu']
    platform_id = request.GET['platform_id']

    DB_platform.objects.filter(id=platform_id).update(monitor_time=monitor_time,
                                                      monitor_phone=monitor_phone,
                                                      monitor_email=monitor_email,
                                                      monitor_feishu=monitor_feishu
                                                      )
    return HttpResponse('')

# 保存旧端
def save_old_platform(request):
    name = request.GET['name']
    host = request.GET['host']
    user = request.GET['user']
    max_Concurrency = request.GET['max_Concurrency']
    platform_id = request.GET['platform_id']

    DB_platform.objects.filter(id=platform_id).update(name=name,
                                                      host=host,
                                                      user=user,
                                                      max_Concurrency=max_Concurrency
                                                      )
    return HttpResponse('')

# 上传脚本
def upload_py(request, cid):
    # 拿到端 id
    platform_id = DB_case.objects.filter(id=cid)[0].platform_id
    # 获取到上传的脚本
    myFile = request.FILES.get("fileUpload",None)
    if not myFile:
        return HttpResponseRedirect('/case_list/%s/'%platform_id)
    file_name = str(myFile)
    fp = open('MyClient/client_%s/cases/%s'%(platform_id,file_name),'wb+')
    for i in myFile.chunks():
        fp.write(i)
    fp.close()
    # 更新用例的数据库
    DB_case.objects.filter(id=cid).update(py=file_name)
    # 返回
    return HttpResponseRedirect('/case_list/%s/'%platform_id)

# 执行脚本
def run_case(request):
    case_id = request.GET['case_id']
    case = DB_case.objects.filter(id=case_id)[0]
    platform_id = case.platform_id
    py = case.py
    if py in ['',None,' ','None']:
        return HttpResponse('Error')
    subprocess.call('python3 MyClient/client_%s/cases/%s'%(platform_id,py),shell=True)

    return HttpResponse('')

# 并发用例
def bf_case(request,did):
    # 所有需要并发的case先拿出来
    cases = DB_case.objects.filter(platform_id=did,Concurrency=True)
    max_bf = DB_platform.objects.filter(id = did)[0].max_Concurrency


    def do_case(case): # 线程要运行的函数
        subprocess.call('python3 MyClient/client_%s/cases/%s' % (case.platform_id,case.py),shell=True)
        print('执行完：',case.name)

    ts =[] # 声明空的线程池
    for case in cases:
        if case.py not in ['',None,' ','None']:
            t = threading.Thread(target=do_case,args=(case,)) # 声明子线程
            t.setDaemon(True) # 设置守护线程
            ts.append(t) # 添加到线程池
    for i in range(0,len(ts),max_bf):
        tmp = ts[i:i+max_bf]
        for t in tmp: # 启动线程
            t.start()
        for t in tmp: # 让主线程等待
            t.join()

    time.sleep(1)
    print("全部执行完毕")
    return HttpResponse('')

# 启动监控
def start_monitor(request, did):
    # 判断监控线程是否已经启动
    try:
        subprocess.check_output('ps -ef|grep "monitor.py %s WEB"|grep -v "grep"' % did,shell=True)
        print("监控已经启动")
        return HttpResponseRedirect('/case_list/'+did+'/')
    except:
        print("监控无，可以启动")
    # 如果没启动，启动
    def start_server():
        subprocess.call('python3 Myapp/monitor.py %s WEB' % did,shell=True)
    t = threading.Thread(target=start_server)
    t.setDaemon(True)
    t.start()
    # 返回
    return HttpResponseRedirect('/case_list/'+did+'/')


# 关闭监控
def stop_monitor(request, did):
    # 找到监控线程
    try:
        cop = subprocess.check_output('ps -ef|grep "monitor.py %s WEB"|grep -v "grep"' % did, shell=True)
        print("监控已经启动，即将停止")
        ports = re.findall(r'(\d+)',str(cop))
        max_id = max([int(i) for i in ports])
        subprocess.call('kill -9 %s'%str(max_id),shell=True)
        print("服务停止")
        # 杀掉监控

    except:
        print("监控无，无需停止")

    return HttpResponseRedirect('/case_list/' + did + '/')






