import json

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from apps.orders.models import OrderInfo, OrderGoods
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

from django.utils import timezone



class OrderCommitView(LoginRequiredJSONMixin, View):
    def post(self, request):
        # 必须是登录用户   user
        user = request.user
        # 接收参数  address_id, pay_method
        data = json.loads(request.body.decode())
        # 提取参数
        address_id = data.get('address_id')
        pay_method = data.get('pay_method')
        # 验证参数
        try:
            address = Address.objects.get(id=address_id)
        except:
            return JsonResponse({'code': 400, 'errmsg': "没有地址"})
        if pay_method not in [1, 2]:
            return JsonResponse({'code': 400, 'errmsg': "支付方式不正确"})
        # 数据入库
        # 先保存订单基本信息
        # 生成订单id  order_id
        order_id = timezone.localtime().strftime('%Y%m%d%H%M%S') + '%09d' % user.id
        # 根据支付方式设置订单状态
        # 1 和 2 代表模型中的支付方式和状态
        if pay_method == 1:
            status = 2
        else:
            status = 1
        # 运费
        from decimal import Decimal
        freight = Decimal('10')
        # 订单总数量和订单总金额（遍历商品id获得数据计算金额）（是重复操作，所以初始值设为0，后期再进行更新）
        total_count = 0
        total_amount = Decimal('10')
        # 应用事物
        from django.db import transaction
        with transaction.atomic():
            # 开始事物
            start_point = transaction.savepoint()
            order = OrderInfo.objects.create(
                order_id=order_id,
                user=user,
                address=address,
                total_count=total_count,
                total_amount=total_amount,
                freight=freight,
                pay_method=pay_method,
                status=status
            )
            # 保存商品信息

            # 连接redis
            redis_cli = get_redis_connection('carts')
            # 获取选中商品id
            selected_ids = redis_cli.smembers('selected_%s' % user.id)
            # 获取hash 数据（数量）{sku_id:count}
            sku_id_counts = redis_cli.hgetall('carts_%s' % user.id)
            # 遍历选中商品的id
            for id in selected_ids:
                # 查询商品的详细信息
                sku = SKU.objects.get(id=id)
            # 获取库存，判断用户购买的数量是否满足库存剩余
            mysql_stock = sku.stock
            custom_count = int(sku_id_counts[id])
            # 不满足，下单失败
            if custom_count > mysql_stock:
                # 进行回滚
                transaction.savepoint_rollback(start_point)
                return JsonResponse({'code': 400, 'errmsg': "下单失败"})
            import time
            time.sleep(7)
            # 模拟并发
            # 记录之前的值
            old_stock = sku.stock
            #　更新数据之前判断记录的值是否和现在查询的值一致
            new_stock = sku.stock - custom_count
            new_sales = sku.sales + custom_count

            result = SKU.objects.filter(id=id, stock=old_stock).update(sales=new_sales, stock=new_stock)
            if result == 0:
                transaction.savepoint_rollback(start_point)
                return JsonResponse({'code': 400, 'errmsg': '下单失败，库存不足'})
            # # 如果满足销量增加，库存减少
            # sku.sales += custom_count
            # sku.stock -= mysql_stock
            # # 保存订单商品信息
            # sku.save()
            # 统计订单总数和订单金额
            OrderGoods.objects.create(
                order=order,
                sku=sku,
                count=custom_count,
                price=sku.price
            )
            # 进行订单基本数据更新
            # 数量统计
            order.total_count += custom_count
            # 价钱统计
            order.total_amount += (custom_count * sku.price)
            # 保存数据
            order.save()
            # 清楚redis中选中的商品
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'order_id': order_id})
        # 返回响应
