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

    def put(self,request):
        # 获取用户
        user = request.user
        # 接受信息
        data =json.loads(request.body.decode())
        # 提取数据
        sku_id = data.get('sku_id')
        count = data.get('count')
        selected = data.get('selected')
        # 验证数据
        try:
            sku =SKU.objects.get(id =sku_id)
        except:
            return JsonResponse({'code':400,'errmsg':'没有此商品'})
        # 更新数据
        # 连接redis
        redis_cli = get_redis_connection('carts')
        # 更新hash数据
        redis_cli.hset('carts_%s' % user.id, sku_id, count)
        # 更新set
        if selected:
            # 选中
            # 添加到 集合中
            redis_cli.sadd('selected_%s' % user.id, sku_id)
        else:
            # 未选中
            # 应该从集合中 移除
            """
            SREM key member [member ...]
            移除集合 key 中的一个或多个 member 元素，不存在的 member 元素会被忽略。
            """
            redis_cli.srem('selected_%s' % user.id, sku_id)
            # 5. 返回响应 为了确保 前后端数据一致,我们要把后端的数据,再告诉前端
        cart_sku = {
            'id': sku_id,
            'name': sku.name,
            'count': count,
            'selected': selected,
            'price': sku.price,
            'amount': sku.price * int(count),
            'default_image_url': sku.default_image.url
        }
        return JsonResponse({'code': 0, 'cart_sku':cart_sku, 'errmsg': 'ok'})


