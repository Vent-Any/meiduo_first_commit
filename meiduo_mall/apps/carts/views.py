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
            sku = SKU.objects.get(id= sku_id)
        except :
            return JsonResponse({'code':400, 'errmsg':"没有这个商品"})
        try:
            count = int(count)
        except:
            count = 1
        # 将数据存入数据库
        # 连接redis数据库
        redis_cli =get_redis_connection('carts')
        # 进行hash表数据存储
        redis_cli.hset('carts_%s' %user.id, sku_id, count)
        # 进行集合数据存储
        redis_cli.sadd('selected_%s'%user.id, sku_id)

        # 返回响应
        return JsonResponse({'code':0,'errmsg':'ok'})

    def get(self,request):

        # 获取用户信息
        user = request.user
        # 连接数据库
        redis_cli = get_redis_connection('carts')
        # 获取hash数据
        sku_id_counts = redis_cli.hgetall('carts_%s'%user.id)
        # 获取集合中的数据
        selected_ids = redis_cli.smembers('selected_%s' % user.id)
        # 获取所有购物车商品的id
        ids = sku_id_counts.keys()
        # 创建一个空数组
        carts_sku = []
        # 遍历商品id
        for id in ids:
            # 根据商品id查询数据
            sku = SKU.objects.get(id=id)
            print(sku)
            #将对象转换成字典
            carts_sku.append({
                'id': sku.id,
                'name': sku.name,
                'price': sku.price,
                'default_image_url': sku.default_image.url,
                'count': int(sku_id_counts[id]),
                'selected': id in selected_ids,
                'amount': sku.price * int(sku_id_counts[id])
            })
        # 返回响应
        return JsonResponse({'code':0, 'errmsg':'ok', 'cart_skus':carts_sku})

