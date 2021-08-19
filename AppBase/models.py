from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
# Create your models here.

# 属性或方法	说明
# username	用户名（必要）
# password	密码（必要）
# email	邮件
# first_name	名字
# last_name	姓氏
# is_staff	是否管理员
# create()	创建一个普通用户
# create_user()	创建一个普通用户，密码加密
# create_superuser()	创建一个超级用户（email必要）
# set_password(pwd)	设置密码
class UserDict(AbstractUser):#用户信息字典
    phone = models.CharField(max_length=32, verbose_name='手机号码')
    img = models.ImageField(upload_to='userimage', default='userimage/qq.jpg', verbose_name='用户头像')
    lvl = models.IntegerField(verbose_name='会员等级', default=0)
    role = models.CharField(max_length=32, verbose_name='角色',default="sa")
    class_name=models.CharField(max_length=32, verbose_name='班级id',default="")
    create_time = models.DateTimeField(verbose_name='创建时间', default=timezone.now)
    class Meta:
        verbose_name=verbose_name_plural="用户字典"
    def __str__(self):
        return self.username

class AppSettings(models.Model):#系统设置
    key = models.CharField(max_length=128, verbose_name='配置项名')
    value = models.CharField(max_length=128, verbose_name='值')
    description=models.CharField(max_length=128, verbose_name='配置描述')
    class Meta:
        verbose_name=verbose_name_plural="系统配置"
    def __str__(self):
        return self.key

class EmailSendFromDefaultSettings(models.Model):#邮件
    id = models.AutoField(primary_key=True)  # 自定义自增列
    smtpServer= models.CharField(verbose_name='使用的SMTP服务', max_length=256, default="")
    formUser=models.CharField(verbose_name='发件人', max_length=256, default="")
    userPassword=models.CharField(verbose_name='发件人邮件授权登录密码', max_length=256, default="")
    userShowName=models.CharField(verbose_name='发送邮件显示发件人别名', max_length=256, default="")
    class Meta:
        verbose_name = verbose_name_plural = "邮箱设置"
    def __str__(self):
        return self.smtpServer

class AppDefaultIocn(models.Model):#系统默认图标
    name = models.CharField(max_length=128, verbose_name='名称')
    img = models.ImageField(upload_to='defaultIocn', default='userimage/qq.jpg', verbose_name='头像')
    class Meta:
        verbose_name=verbose_name_plural="默认图标字典"
    def __str__(self):
        return self.name