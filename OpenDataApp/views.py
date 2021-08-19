from AppBase.base import  *
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login,logout
import  random
from AppBase.sendEmail import *
from OpenDataApp import models
# Create your views here.
from OpenDataApp.helper import  TanYanChaApi
#系统配置
class QueryTaxCode(View):
    def post(self,request):
        data=json.loads(request.body)
        compname = data.get('compname',"")#公司全名称
        if compname=="":
            return  failedResponseCommon({},"公司名称不能为空")
        #优先查询数据库
        company_list=models.company_info.objects.filter(Q(name=compname))
        resdata={}
        msg="未找到企业信息，请核实名称"
        if len(company_list)<=0:
            # 查询爬虫接口
            data=TanYanChaApi.GetCompanyNameAddress(compname)
            for item in data:
                if item["name"]==compname:
                    # 存放数据
                    models.company_info.objects.create(name=compname,tax_number=item["sh"],tan_yan_url=item["url"],address=item["address"])
                    resdata={"name":compname,"tax_number":item["sh"],"address":item["address"]}
                    msg="success"
        else:
            item=company_list[0]
            resdata = {"name": compname, "tax_number": item.tax_number, "address": item.address}
            msg = "success"
        if msg=="success":
            return successResponseCommon(resdata, msg)
        else:
            return  failedResponseCommon({},msg)












