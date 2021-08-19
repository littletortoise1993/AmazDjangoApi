
from django.conf.urls import url, include
from AppBase import  views
urlpatterns = [
    url(r"^findpassword$", views.FindPasswordView.as_view(), name="findpassword"),#找回密码
    url(r"^register$", views.RegistAPIView.as_view(), name="register_api"),
    url(r"^login$", views.LoginAPIView.as_view(), name="login_api"),
    url(r"^userdata$", views.UserDataView.as_view(), name="userdata"),

]
