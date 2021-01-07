import http
import json
import re

from QQLoginTool.QQtool import OAuthQQ
from django.contrib.auth import login
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render

# Create your views here.
# QQ登录参数
# 我们申请的 客户端id
from django.views import View
from django_redis import get_redis_connection

from apps.oauth.models import OAuthQQUser
from apps.oauth.utils import generate_access_token, check_access_token
from apps.users.models import User

QQ_CLIENT_ID = '101474184'
# 我们申请的 客户端秘钥
QQ_CLIENT_SECRET = 'c6ce949e04e12ecc909ae6a8b09b637c'
# 我们申请时添加的: 登录成功后回调的路径
QQ_REDIRECT_URI = 'http://www.meiduo.site:8080/oauth_callback.html'

class QQAuthUserView(View):
    """用户扫码登录的回调处理"""

    def get(self, request):
        """Oauth2.0认证"""
        # 接收Authorization Code
        code = request.GET.get('code')
        if not code:
            return HttpResponseBadRequest('缺少code')
        oauth = OAuthQQ(client_id=QQ_CLIENT_ID,
                        client_secret=QQ_CLIENT_SECRET,
                        redirect_uri=QQ_REDIRECT_URI)
        # 使用code请求access_token
        access_token = oauth.get_access_token(code)
        # 使用access_token 换取openid
        openid =oauth.get_open_id(access_token)
        # 判断openi是否绑定用户
        try:
            oauth_user = OAuthQQUser.objects.get(openid=openid)
        except :
            access_token = generate_access_token({'openid': openid})
            # 注意: 这里一定不能返回 0 的状态码. 否则不能进行绑定页面
            return JsonResponse({'code': 300, 'errmsg': 'ok', 'access_token': access_token})

        else:
            user = oauth_user.user
            # 实现状态保持
            login(request, user)

            # 创建重定向到主页的对象
            response = JsonResponse({'code': 0, 'errmsg': 'ok'})

            # 将用户信息写入到 cookie 中，有效期14天
            response.set_cookie('username', user.username, max_age=3600 * 24 * 14)
            # 返回响应
            return response

    def post(self, request):
        """美多商城用户绑定到openid"""

        # 1.接收参数
        data_dict = json.loads(request.body.decode())
        mobile = data_dict.get('mobile')
        password = data_dict.get('password')
        sms_code_client = data_dict.get('sms_code')
        access_token = data_dict.get('access_token')

        # 2.校验参数
        # 判断参数是否齐全
        if not all([mobile, password, sms_code_client]):
            return JsonResponse({'code': 400,
                                      'errmsg': '缺少必传参数'})

        # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({'code': 400,
                                      'errmsg': '请输入正确的手机号码'})

        # 判断密码是否合格
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return JsonResponse({'code': 400,
                                      'errmsg': '请输入8-20位的密码'})

        # 3.判断短信验证码是否一致
        # 创建 redis 链接对象:
        redis_conn = get_redis_connection('code')

        # 从 redis 中获取 sms_code 值:
        sms_code_server = redis_conn.get('sms_%s' % mobile)

        # 判断获取出来的有没有:
        if sms_code_server is None:
            # 如果没有, 直接返回:
            return JsonResponse({'code': 400,
                                      'errmsg': '验证码失效'})
        # 如果有, 则进行判断:
        if sms_code_client != sms_code_server.decode():
            # 如果不匹配, 则直接返回:
            return JsonResponse({'code': 400,
                                      'errmsg': '输入的验证码有误'})

            # 调用我们自定义的函数, 检验传入的 access_token 是否正确:
        # 错误提示放在 sms_code_errmsg 位置
        openid = check_access_token(access_token)
        if not openid:
            return JsonResponse({'code': 400,
                                      'errmsg': '缺少openid'})
        # 4.保存注册数据
        try:
            user = User.objects.get(mobile=mobile)
        except :
            # 用户不存在,新建用户
            user = User.objects.create_user(username=mobile,
                                            password=password,
                                            mobile=mobile)
        else:
            # 如果用户存在，检查用户密码
            if not user.check_password(password):
                return JsonResponse({'code': 400,
                                          'errmsg': '输入的密码不正确'})
        # 5.将用户绑定 openid
        try:
            OAuthQQUser.objects.create(openid=openid,
                                       user=user)
        except :
            return JsonResponse({'code': 400,
                                      'errmsg': '往数据库添加数据出错'})
        # 6.实现状态保持
        login(request, user)

        # 7.创建响应对象:
        response = JsonResponse({'code': 0,
                                      'errmsg': 'ok'})

        # 8.登录时用户名写入到 cookie，有效期14天
        response.set_cookie('username',
                            user.username,
                            max_age=3600 * 24 * 14)

        # 9.响应
        return response