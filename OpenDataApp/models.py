from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
# Create your models here.
from AppBase.models import UserDict

#企业信息表

class company_info(models.Model):#邮件
    id = models.AutoField(primary_key=True)  # 自定义自增列
    name= models.CharField(verbose_name='企业名称', max_length=256, default="")
    tax_number= models.CharField(verbose_name='企业税号', max_length=256, default="")
    tan_yan_url=models.CharField(verbose_name='企业详情url', max_length=256, default="")
    address = models.CharField(verbose_name='企业地址', max_length=256, default="")
    create_time=models.DateTimeField(verbose_name='创建时间', default=timezone.now)
    update_time=models.DateTimeField(verbose_name='更新时间', default=timezone.now)
    data_flag=models.IntegerField(verbose_name="数据标记",default=0)
    class Meta:
        verbose_name = verbose_name_plural = "企业信息主表"
    def __str__(self):
        return self.name


