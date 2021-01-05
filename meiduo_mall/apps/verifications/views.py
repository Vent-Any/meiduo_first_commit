from django.shortcuts import render
from django.views import View
from libs.captcha.captcha import captcha
from django.http import JsonResponse,HttpResponse
from django_redis import get_redis_connection
# Create your views here.
class ImageCodeView(View):
    def get(self, request, uuid):
        # 生成图片验证码
        text, image = captcha.generate_captcha()
        # 保存图片验证码
        redis_conn = get_redis_connection('code')
        redis_conn.setex('img_%s' % uuid, 300, text)
        # 响应图片验证码
        return HttpResponse(image, content_type='image/jpeg')

