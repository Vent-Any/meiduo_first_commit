from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from utils.views import LoginRequiredJSONMixin
from apps.users.models import Address
from django_redis import get_redis_connection
from apps.goods.models import SKU


# 提交订单页面展示
class OrderSubmitView(LoginRequiredJSONMixin, View):

    def get(self, request):
        # 获取用户信息
        user = request.user
        # 1. 获取地址信息
        #     1.1 查询登录用户的地址信息
        addresses=Address.objects.filter(user=user,is_deleted=False)
        #     1.2 将对象列表转换为字典列表
        addresses_list=[]
        for address in addresses:
            addresses_list.append({
                'id': address.id,
                'province': address.province.name,
                'city': address.city.name,
                'district': address.district.name,
                'place': address.place,
                'receiver': address.receiver,
                'mobile': address.mobile
            })
        # 2. 获取购物车中选中商品信息
        #     2.1 连接redis
        redis_cli=get_redis_connection('carts')
        #     2.2 获取set  选中商品的id
        selected_ids=redis_cli.smembers('selected_%s'%user.id)
        #     2.3 获取hash    所有商品的id 和数量
        sku_id_counts=redis_cli.hgetall('carts_%s'%user.id)
        #     2.4 遍历选中商品的id
        selected_carts=[]
        for id in selected_ids:
            #     2.5 查询商品信息
            sku = SKU.objects.get(id=id)
            #     2.6 将对象转换为字典(记得添加购物车数量)
            selected_carts.append({
                'id':sku.id,
                'name':sku.name,
                'default_image_url': sku.default_image.url,
                'count': int(sku_id_counts[id]),
                'price':sku.price
                # 'amount': sku.price*int(sku_id_counts[id])
            })
        # 3. 运费
        freight = 10
        # 4. 组织数据返回响应
        context = {
            'addresses':addresses_list,
            'skus':selected_carts,
            'freight':freight
        }

        return JsonResponse({'code':0,'errmsg':'ok','context':context})
