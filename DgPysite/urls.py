"""DgPysite URL Configuration

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
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from AppBase.views import error404
from django.core.cache import cache #引入缓存模块
cache.set('zhouqx', '123456', 30*60)      #写入key为key，值为value的缓存，有效期30分钟
cache.has_key('zhouqx') #判断key为k是否存在
cache.get('zhouqx')     #获取key为k的缓存
urlpatterns = [
                  url(r"^admin", admin.site.urls),  # DjangoAdmin后台管理路由
                  url(r"^baseapi/", include("AppBase.urls")),
                  url(r"^clound-api/", include("OpenDataApp.urls")),#在线考试教育路由转发
                  url(r"^(?!media)", error404, name="error404"),  # 排除图片资源 其他未定义转到404错误页面  (django自带404错误调试模式不能用)
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 静态图片资源路径
