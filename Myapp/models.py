from django.db import models

# Create your models here.
# ORM连接数据库
class DB_href(models.Model): # 超链接表
    name = models.CharField(max_length=20, null=True, blank=True)
    url = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name #

class DB_platform(models.Model): # 平台表
    name = models.CharField(max_length=20, null=True, blank=True)
    monitor_time = models.CharField(max_length=200, null=True, blank=True) # 监控时间
    monitor_phone = models.CharField(max_length=200, null=True, blank=True) # 电话
    monitor_email = models.CharField(max_length=200, null=True, blank=True) # 邮件
    monitor_feishu = models.CharField(max_length=200, null=True, blank=True) # 飞书通知

    host = models.CharField(max_length=500, null=True, blank=True)

    user = models.CharField(max_length=20, null=True, blank=True)
    max_Concurrency = models.IntegerField(default=5)# 最大并发次数

    def __str__(self):
        return self.name

class DB_case(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True, default='-')
    platform_id = models.CharField(max_length=20, null=True, blank=True)
    Concurrency = models.BooleanField(default=True) # 参与并发
    monitor = models.BooleanField(default=True) # 参与监控
    py = models.CharField(max_length=20, null=True, blank=True) # 绑定脚本名称
    counts = models.IntegerField(default=1) # 用例失败重试次数

    def __str__(self):
        return self.name


