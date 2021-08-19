from AppBase.base import  *
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login,logout
import  random
from AppBase.sendEmail import *
# Create your views here.

#注册api
class RegistAPIView(View):
    def post(self,request):
        username = request.POST.get('name',"")
        useremail = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        if username=="":
            username=useremail
        if not all([useremail, password]):
            return errorResponseCommon({},"用户名或密码未输入")
        # 判断名字是否已存在
        users = models.UserDict.objects.filter(Q(username=username) | Q(email=useremail))
        if len(users) <= 0:
            # 邮箱验证发送邮件
            res = SendEmail(useremail, "感谢注册电商", "网站后续完善中，后续更多精彩，敬请期待！")
            if res == "success":
                # 随机头像
                iocnList = models.AppDefaultIocn.objects.all()
                if len(iocnList) > 0:
                    iocnIndex = random.randint(0, len(iocnList)-1)
                    user = models.UserDict.objects.create_user(username=username, email=useremail, phone="",role=role,
                                                               password=password, img=iocnList[iocnIndex].img)
                else:
                    user = models.UserDict.objects.create_user(username=username, email=useremail, phone="",role=role,
                                                               password=password)
                login(request, user)  # 用户登录
                return successResponseCommon({}, "注册成功")
            else:
                return errorResponseCommon({}, "邮箱验证失败！")



        else:
            #精确提示什么已被注册
            if len(models.UserDict.objects.filter(Q(username=username)))>0:
                return errorResponseCommon({}, "用户名已被注册")
            return errorResponseCommon({},"邮箱已被注册")

#登录验证api
class LoginAPIView(View):
    def post(self,request):
        data=json.loads(request.body)
        username = data.get('username',"")
        # 判断用户名 密码是否合法用户
        password = data.get('password',"")
        # 进行数据校验
        if not all([username, password]):
            return errorResponseCommon({},"用户名或密码未输入")
        #根据输入username(可以是邮箱 手机号码 用户名 三者都是唯一值)查询username
        try:
            user = models.UserDict.objects.get(Q(phone=username) | Q(email=username) | Q(username=username))
        except models.UserDict.DoesNotExist:  # 可以捕获除与程序退出sys.exit()相关之外的所有异常
            return errorResponseCommon({},"用户不存在")
        #验证密码
        user = authenticate(username=user.username, password=password)  # 用户验证
        if user:
            login(request, user)  # 用户登录
            #生成token
            token = get_token(username)
            return ResponseUserData(user,token)
        return errorResponseCommon({},"密码错误")

#找回密码
class FindPasswordView(View):
    def post(self,request):
        # 找回密码
        email = request.POST.get('email', "")
        try:
            u = models.UserDict.objects.get(email=email)
        except models.UserDict.DoesNotExist:  # 可以捕获除与程序退出sys.exit()相关之外的所有异常
            return errorResponseCommon({}, "邮箱未注册")
        code = "".join([str(random.randint(0, 9)) for _ in range(6)])
        u.set_password(code)
        u.save()
        res = SendEmail(email, "密码找回", "您的登录密码已重置为：" + code)
        if res == "success":
            return successResponseCommon({},"密码已发送到您的邮箱！")
        else:
            return errorResponseCommon({},"密码找回失败")

@method_decorator(checkLogin, name='dispatch')
class UserDataView(View):
    def post(self,request):
        return ResponseUserData(request.user,request.headers.get("token", ""))



###统一返回用户信息和token
def ResponseUserData(user,token):
    data = {"token":token, "userName": user.username, "email": user.email, "phone": user.phone,
            "id": user.id,"avatar":user.img.url,"roles":['student', 'sa','teacher'],"realName":"","introduction":""}
    return successResponseCommon(data)








def error404(request):
    return notFoundResponseCommon({},"未找到路由")









#用户信息页面
@method_decorator(checkLogin, name='dispatch')
class UserInfoView(View):
    def get(self, request):
        id = request.GET.get("id", 0)
        if id==0:
            id=request.user.id
        return render(request, "user_info.html", {"id": id})

#用户数据
class UserInfoDataView(View):
    def get(self, request):
        id = request.GET.get("id", 0)
        user=UserDict.objects.get(id=id)
        data={"id":user.id,"username":user.username,"email":user.email,"phone":user.phone,"img":user.img.url}
        return successResponseCommon(
            {"items": data, "pages": 1, "curpage": 1,
             "sumNum": 1,
             "nodataflag": 1})
    def post(self,request):
        #修改用户信息
        data = request.POST
        id = data.get('id', 0)
        username = data.get("username", "")
        email = data.get("email", "")
        phone = data.get("phone", "")
        psd = data.get("psd", "")
        dataitem = models.UserDict.objects.get(id=id)
        dataitem.username = username
        if psd != "123456":
            dataitem.set_password(psd)
        dataitem.email = email
        dataitem.phone = phone
        if request.FILES:
            pic = request.FILES.get('pic')
            dataitem.img = pic
        dataitem.save()
        return successResponseCommon({}, "修改成功！")
