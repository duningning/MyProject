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
    monitor_time = models.CharField(max_length=20, null=True, blank=True) # 监控
    url = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name
