from QQLoginTool.QQtool import OAuthQQ
from django.views import View
from django.http import *

class QQUserView(View):
    """用户扫码登录的回调处理"""
    def get(self, request):
        code = request.GET.get('code')
        if code is None:
            return JsonResponse({'code':400, 'errmsg':"没有code参数"})
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
            pass
        else:
            from django.contrib.auth import login
            login(request, qquser.user)
            response = JsonResponse({'code':0, 'errmsg':"OK"})
            response.set_cookie('username',qquser.user.username, max_age=14*24*3600)

