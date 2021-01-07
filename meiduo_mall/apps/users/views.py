from django.contrib.auth import authenticate
from django.shortcuts import render

# Create your views here.
from django.views import View
from apps.users.models import User
from django.http import JsonResponse
import json


class UsernameCountView(View):
    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        return JsonResponse({'code': 0, 'errmsg': 'OK', 'count': count})

class MobileCountView(View):
    def get(self,request, mobile):
        count = User.objects.filter(mobile=mobile).count()
        return JsonResponse({'code': 0, 'errmsg': 'OK', 'count': count})


class RegisterView(View):
    def post(self, request):
        data_b = request.body
        data_b = data_b.decode()
        data = json.loads(data_b)
        # 获取参数
        username = data.get('username')
        password = data.get('password')
        password2 = data.get('password2')
        mobile = data.get('mobile')
        allow = data.get('allow')
        sms_code = data.get('sms_code')
# 校验参数
        from django import http
        import re
        # 判断参数是否齐全
        if not all([username, password, password2, mobile, allow]):
            return http.JsonResponse({'code': 400, 'errmsg':'缺少必传参数!'})
        # 判断用户名是否是5-20个字符
        if not re.match(r'^[a-zA-Z0-9_]{5,20}$', username):
            return http.JsonResponse({'code': 400, 'errmsg': 'username格式有误!'})
        # 判断密码是否是8-20个数字
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return http.JsonResponse({'code': 400, 'errmsg': 'password格式有误!'})
        # 判断两次密码是否一致
        if password != password2:
            return http.JsonResponse({'code': 400, 'errmsg': '两次输入不对!'})
        # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.JsonResponse({'code': 400, 'errmsg': 'mobile格式有误!'})
        # 判断是否勾选用户协议
        if allow != True:
            return http.JsonResponse({'code': 400, 'errmsg': 'allow格式有误!'})
#   保存参数
        user = User.objects.create_user(username=username,
                                        password=password,
                                        mobile=mobile)
        from django.contrib.auth import login
        # 参数一  请求对象
        # 参数二  用户信息
        login(request, user)
        # 返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok'})

class LoginView(View):
    def post(self, request):
        dict =json.loads(request.body.decode())
        username = dict.get('username')
        password = dict.get('password')
        remembered = dict.get('remembered')
        if not all([username, password]):
            return JsonResponse({'code': 400, 'errmsg': "缺少参数"})
        # 验证是否能够登录
        user = authenticate(username=username, password=password)
        if user is None:
            return JsonResponse({'code': 400, 'errmsg': "无法登陆"})
        if remembered != True:
            request.session.set_expiry(0)
        else:
            request.session.ser_expiry(None)

        return JsonResponse({'code': 400, 'errmsg': "OK"})



