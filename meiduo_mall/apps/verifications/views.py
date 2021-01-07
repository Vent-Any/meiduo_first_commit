from django.shortcuts import render
from django.views import View
from libs.captcha.captcha import captcha
from django.http import JsonResponse, HttpResponse
from django_redis import get_redis_connection
import logging
import random


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


# 短信验证
class SMSCodeView(View):
    def get(self, request, mobile):
        # 接受请求
        image_conn_client = request.GET.get('image_code')
        uuid = request.GET.get('image_code_id')
        # 校验参数
        if not all([image_conn_client, uuid]):
            return HttpResponse({'code': 400, 'errmsg': '缺少参数'})
        # 创建连接到redis的对象
        redis_conn = get_redis_connection('code')
        # 提取图形验证码
        image_code_server = redis_conn.get('img_%s' % uuid)
        if image_code_server is None:
            return JsonResponse({'code': 400, 'errmsg': '图形验证码失效'})
        # 将图形验证码删除 ,避免恶意测试图形验证码
        redis_conn.delete('img_%s' % uuid)

        # 进行图形验证码对比
        if image_conn_client.lower() != image_code_server.decode().lower():
            return JsonResponse({'code': 400, 'errmsg': "输入图形验证码有误"})
        send_flag = redis_conn.get('send_flag_%s' % mobile)
        if send_flag:
            return JsonResponse({'code': 400, 'errmsg': "存在"})
        # 生成短信验证码
        sms_code = '%06d' % random.randint(0, 999999)
        # 保存短信验证码
        # 创建redis管道
        p1 =redis_conn.pipeline()
        p1.setex('sms_%s' % mobile, 300, sms_code)

        from celery_tasks.sms.tasks import sms
        sms.delay(mobile, sms_code)
        # 避免频繁发送短信验证码
        # 通过容联云发送短信
        # import json
        # from ronglian_sms_sdk import SmsSDK
        # accId = '容联云通讯分配的主账号ID'
        # accToken = '容联云通讯分配的主账号TOKEN'
        # appId = '容联云通讯分配的应用ID'
        # sdk = SmsSDK(accId, accToken, appId)
        # tid = '容联云通讯创建的模板ID'
        # mobile = '手机号1,手机号2'
        # datas = ('变量1', '变量2')
        # sdk.sendMessage(tid, mobile, datas)
        p1.setex('send_flag_%s' % mobile, 60, 1)
        p1.execute()
        return JsonResponse({'code': 0, 'errmsg': '发送短信成功'})

