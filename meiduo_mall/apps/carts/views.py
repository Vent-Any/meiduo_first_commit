import json

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from django_redis import get_redis_connection

from apps.goods.models import SKU
from utils.views import LoginRequiredJSONMixin


class CartsView(LoginRequiredJSONMixin, View):
    def post(self,request):
        #获取用户信息
        user =request.user
        # 接受参数
        data = json.loads(request.body.decode())
        # 提取参数
        sku_id = data.get('sku_id')
        count = data.get('count')
        # 验证参数
        if not all([sku_id, count]):
            return JsonResponse({'code':400, 'errmsg':"没有这个商品"})
        try:
            sku = SKU.onjects.get(id= sku_id)
        except:
            return JsonResponse({'code':400, 'errmsg':"没有这个商品"})
        try:
            count = int(count)
        except:
            count = 1
        # 将数据存入数据库
        # 连接redis数据库
        redis_cli =get_redis_connection('carts')
        # 建立管道
        p = redis_cli.pipeline()
        # 进行hash表数据存储
        p.hset('carts_%s' %user.id, sku_id, count)
        # 进行集合数据存储
        p.sadd('selected_%s'%user.id, sku_id)
        # 返回响应
        return JsonResponse({'code':0,'errmsg':'ok'})

