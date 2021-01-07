import http

from QQLoginTool.QQtool import OAuthQQ
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render

# Create your views here.
# QQ登录参数
# 我们申请的 客户端id
from django.views import View

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
        opeid =oauth.get_open_id(access_token)
        return JsonResponse({'code': 0,'errmsg': "回调"})
