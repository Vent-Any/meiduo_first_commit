import re

from django.contrib.auth import authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.views import View
from apps.users.models import User
from django.http import JsonResponse
import json

from utils.views import LoginRequiredJSONMixin


class UsernameCountView(View):
    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        return JsonResponse({'code': 0, 'errmsg': 'OK', 'count': count})


class MobileCountView(View):
    def get(self, request, mobile):
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
            return http.JsonResponse({'code': 400, 'errmsg': '缺少必传参数!'})
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
        dict = json.loads(request.body.decode())
        username = dict.get('username')
        password = dict.get('password')
        remembered = dict.get('remembered')
        if not all([username, password]):
            return JsonResponse({'code': 400, 'errmsg': "缺少参数"})
        # 多账号登录
        if re.match('^1[3-9]\d{9}$', username):
            User.USERNAME_FIELD = 'mobile'
        else:
            User.USERNAME_FIELD = 'username'
        # 验证是否能够登录
        user = authenticate(username=username, password=password)
        if user is None:
            return JsonResponse({'code': 400, 'errmsg': "用户名或者密码错误"})
        from django.contrib.auth import login
        login(request, user)
        if remembered != True:
            request.session.set_expiry(0)
        else:
            request.session.set_expiry(None)
        response = JsonResponse({'code': 0, 'errmsg': "OK"})
        response.set_cookie('username', username, max_age=14*24*3600)
        return response

class logoutView(View):
    def delete(self, request):
        # 清理Session
        logout(request)
        response = JsonResponse({'code': 0, 'errmsg': "OK"})
        response.delete_cookie('username')
        return response


class UserInfoView(LoginRequiredJSONMixin, View):
    """用户中心"""

    def get(self, request):
        print(1111111111111111111111)
        """提供个人信息界面"""
        user = request.user
        # 获取界面需要的数据,进行拼接
        user_info = {
            'username':user.username,
            'mobile': user.mobile,
            'email': user.email,
            'email_active': False
        }

        # 返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'info_data': user_info})


class EmailView(View):
    def put(self, request):
        # put 请求的内容也在body中
        # 接受请求
        data = json.loads(request.body.decode())
        # 提取参数
        email =data.get('email')
        # 更新数据 保存到数据库
        user = request.user
        user.email = email
        user.save()
        return JsonResponse({'code': 0})


