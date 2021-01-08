from QQLoginTool.QQtool import OAuthQQ
from django.views import View
from django.http import *


class QQUserView(View):
    """用户扫码登录的回调处理"""

    def get(self, request):
        code = request.GET.get('code')
        if code is None:
            return JsonResponse({'code': 400, 'errmsg': "没有code参数"})
        # QQ登录参数
        # 我们申请的 客户端id
        QQ_CLIENT_ID = '101474184'
        # 我们申请的 客户端秘钥
        QQ_CLIENT_SECRET = 'c6ce949e04e12ecc909ae6a8b09b637c'
        # 我们申请时添加的: 登录成功后回调的路径
        QQ_REDIRECT_URI = 'http://www.meiduo.site:8080/oauth_callback.html'
        qq = OAuthQQ(client_id=QQ_CLIENT_ID,
                     client_secret=QQ_CLIENT_SECRET,
                     redirect_uri=QQ_REDIRECT_URI)
        # 使用code换取token
        access_token = qq.get_access_token(code)
        # 使用token换取openid
        openid = qq.get_open_id(access_token)
        from apps.oauth.models import OAuthQQUser
        # 根据openid进行判断
        try:
            qquser = OAuthQQUser.objects.get(openid=openid)
        except:
            from apps.oauth.utils import generate_access_token
            token = generate_access_token(openid)
            return JsonResponse({'code': 300, 'access_token': token})
        else:
            from django.contrib.auth import login
            login(request, qquser.user)
            response = JsonResponse({'code': 0, 'errmsg': "OK"})
            response.set_cookie('username', qquser.user.username, max_age=14 * 24 * 3600)
            return response

    def post(self, request):
        import json
        data = json.loads(request.body.decode())
        mobile = data.get('mobile')
        password = data.get('password')
        sms_code = data.get('sms_code')
        access_token = data.get('access_token')
        from apps.oauth.utils import check_access_token
        openid = check_access_token(access_token)
        if openid is None:
            return JsonResponse({'code': 400, 'errmsg': "绑定失败"})
        # 根据手机号判断用户信息
        from apps.users.models import User
        try:
            user = User.objects.get(mobile=mobile)
        except:
            user = User.objects.create_user(username=mobile,
                                            mobile=mobile,
                                            password=password)
        else:
            if not user.check_password(password):
                return JsonResponse({'code': 400, 'errmsg': "绑定失败"})
            # 绑定用户信息
            from apps.oauth.models import OAuthQQUser
            OAuthQQUser.objects.create(openid=openid, user=user)
            # 状态保持
            from django.contrib.auth import login
            login(request, user)
            # 设置cookie
            response = JsonResponse({'code': 0, 'errmsg': 'OK'})
            response.set_cookie('username', user.username, max_age=14 * 24 * 3600)
            return response
