"""MyProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from Myapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home), # 设置进入首页url
    path('', home),  # 设置进入首页url
    path('save_platform/', save_platform),  # 保存新端
    re_path('del_platform/(?P<did>.+)/', del_platform),  # 删除端
    re_path('case_list/(?P<did>.+)/',  case_list),  # 进入用例列表页
    re_path('add_case/(?P<did>.+)/', add_case), # 添加用例
    re_path('del_case/(?P<cid>.+)/', del_case),  # 删除用例
    path('set_case/', set_case),  # 获取用例数据
    path('save_case/', save_case),  # 保存用例数据
    # path('set_monitor/', set_monitor),  # 获取监控设置
    path('save_monitor/', save_monitor),  # 保存监控设置
    path('save_old_platform/', save_old_platform),  # 保存旧端的设置

    re_path('upload_py/(?P<cid>.+)/',upload_py),  # 上传脚本
    path('run_case/',run_case), # 执行脚本

    re_path('bf_case/(?P<did>.+)/', bf_case),  # 并发用例
    re_path('start_monitor/(?P<did>.+)/', start_monitor),  # 启动监控
    re_path('stop_monitor/(?P<did>.+)/', stop_monitor),  # 停止监控
]
