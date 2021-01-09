import re

from django.contrib.auth import authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.views import View
from apps.users.models import User, Address
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
        response.set_cookie('username', username, max_age=14 * 24 * 3600)
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
        """提供个人信息界面"""
        user = request.user
        # 获取界面需要的数据,进行拼接
        user_info = {
            'username': user.username,
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
        email = data.get('email')
        # 更新数据 保存到数据库
        user = request.user
        user.email = email
        user.save()
        # token 数据是一个加密的数据,这个数据中 包含用户信息就可以
        from apps.users.utils import generic_user_id
        token = generic_user_id(user.id)
        verify_url = 'http://www.meiduo.site:8080/success_verify_email.html?token = %s' % token
        # html_message = '<p>尊敬的用户您好！</p>' \
        #                '<p>感谢您使用美多商城。</p>' \
        #                '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
        #                '<p><a href="%s">%s<a></p>' % (email, verify_url, verify_url)
        # celery 方式发送 接口实现
        from celery_tasks.email.tasks import celery_send_email
        celery_send_email.delay(email, verify_url)
        # 返回响应
        return JsonResponse({'code': 0, 'errmsg': 'OK'})


#          ------      验证邮箱    --------
class VerifyEmailView(View):
    def put(self, request):
        """
        1. 接收请求
        2. 提取数据
        3. 对数据进行解密操作
        4. 判断有没有user_id
        5. 如果没有则说明 token过期了
        6. 如果有,则查询用户信息11.省市区模型
        7. 改变用户的邮箱激活状态
        8. 返回响应
        :param request:
        :return:
        """
        # 1. 接收请求
        data = request.GET
        # 2. 提取数据
        token = data.get('token')
        # 3. 对数据进行解密操作
        from apps.users.utils import check_user_id
        user_id = check_user_id(token)
        # 4. 判断有没有user_id
        if user_id is None:
            # 5. 如果没有则说明 token过期了
            return JsonResponse({'code': 400, 'errmsg': '链接时效'})
        # 6. 如果有,则查询用户信息
        try:
            user = User.objects.get(id=user_id)
        except :
            return JsonResponse({'code': 400, 'errmsg': '链接时效'})
        # 7. 改变用户的邮箱激活状态
        user.email_active = True
        user.save()
        # 8. 返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok'})


class CreateAddressView(LoginRequiredJSONMixin, View):
    def post(self, request):
        #  LoginRequiredJSONMixin 用来判断用户是否是登陆的状态.
        # 接受参数
        data = json.loads(request.body.decode())
        receiver = data.get('receiver')
        province_id = data.get('province_id')
        city_id = data.get('city_id')
        district_id = data.get('district_id')
        place = data.get('place')
        mobile = data.get('mobile')
        tel = data.get('tel')
        email = data.get('email')
        # 数据入库
        address =Address.objects.create(
            user=request.user,
            title=receiver,
            receiver=receiver,
            province_id=province_id,
            city_id=city_id,
            district_id=district_id,
            place=place,
            mobile=mobile,
            tel=tel,
            email=email
        )
        # 返回响应 (以字典形式)
        address_dict = {
            'id': address.id,
            "title": address.title,
            "receiver": address.receiver,
            "province": address.province.name,
            "city": address.city.name,
            "district": address.district.name,
            "place": address.place,
            "mobile": address.mobile,
            "tel": address.tel,
            "email": address.email
        }
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'address': address_dict})
