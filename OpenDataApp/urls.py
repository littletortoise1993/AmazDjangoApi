
from django.conf.urls import url, include
from OpenDataApp import  views

urlpatterns = [
    url(r"querytaxcode/v1", views.QueryTaxCode.as_view(), name="querytaxcode")

]
