from django.shortcuts import render
import os
from django.http import JsonResponse
from alipay import AliPay
from alipay.utils import AliPayConfig
from django.views import View
from apps.payment.models import Payment
from meiduo_mall import settings
from utils.views import LoginRequiredJSONMixin
from apps.orders.models import OrderInfo


# Create your views here.
class PayURLView(LoginRequiredJSONMixin, View):
    def get(self, request, order_id):
        # 必须是登录用户
        user = request.user
        #  获取order_id  url中有
        # 根据订单id查询订单信息
        # 为了更准确的进行查询，我们增加一些条件
        try:
            order = OrderInfo.objects.get(order_id=order_id, user=user)
        except:
            return JsonResponse({'code': 400, 'errmsg': "没有此订单"})
        # 创建支付宝对象
        # 通过文件形式来读取美多的私钥支付宝的公钥
        # 我们将公钥和私钥放在setting中 设置一个相对路径
        app_private_key_string = open(settings.APP_PRIVATE_KEY_PATH).read()
        alipay_public_key_string = open(settings.ALIPAY_PUBLIC_KEY_PATH).read()
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,  # 默认回调url
            app_private_key_string=app_private_key_string,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=alipay_public_key_string,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=False,  # 默认False
            config=AliPayConfig(timeout=15)  # 可选, 请求超时时间
        )
        # 我们通过电脑网址支付的方式来生成order_string
        subject = "测试订单"

        # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,  # 美多商城的订单id
            total_amount=str(order.total_amount),  # 订单总金额  类型转换为 str
            subject=subject,
            return_url=settings.ALIPAY_RETURN_URL,  # 支付成功之后,最终要跳转会美多
            # notify_url="https://example.com/notify"  # 可选, 不填则使用默认notify url
        )
        # 5. 拼接url
        alipay_url = 'https://openapi.alipaydev.com/gateway.do?' + order_string

        # 6. 返回支付url
        return JsonResponse({'code': 0, 'alipay_url': alipay_url})


class PaycommitView(View):
    def put(self, request):
        # 获取前端传入的请求参数
        data = request.GET
        # 读取order_id
        out_trade_no = data.get('out_trade_no')
        # 读取支付宝流水号
        trade_no = data.get('trade_no')
        # 保存Payment模型类数据
        Payment.objects.create(
            order_id=out_trade_no,
            trade_id=trade_no
        )
        # 修改订单状态为待评价
        OrderInfo.objects.filter(order_id=out_trade_no, status=OrderInfo.ORDER_STATUS_ENUM['UNPAID']).update(
            status=OrderInfo.ORDER_STATUS_ENUM["UNCOMMENT"])
        # 响应trade_id
        return JsonResponse({'code': 0, 'errmsg': "OK", 'trade_id': trade_no})
