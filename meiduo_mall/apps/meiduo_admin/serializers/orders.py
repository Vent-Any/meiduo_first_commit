from rest_framework import serializers

from apps.goods.models import SKU
from apps.orders.models import OrderInfo, OrderGoods


class OrdersModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderInfo
        fields = '__all__'


class SKUModelSerializer(serializers.ModelSerializer):
    # # 对应外键值
    # category_id = serializers.IntegerField()
    # # 对应模型返回数值
    # category = serializers.StringRelatedField()
    # spu = serializers.StringRelatedField()
    # spu_id = serializers.IntegerField()
    class Meta:
        model = SKU
        fields = ['name', 'default_image']


class OrdersGoodsModelSerializer(serializers.ModelSerializer):
    # 对应外键值
    # order_id = serializers.IntegerField()
    # # 对应模型返回数值
    # order = serializers.StringRelatedField()
    # sku = serializers.StringRelatedField()
    # sku_id = serializers.IntegerField()
    sku = SKUModelSerializer()
    class Meta:
        model = OrderGoods
        fields =['count','price','sku']


class OrderDetailModelSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    skus = OrdersGoodsModelSerializer(many=True)


    class Meta:
        model = OrderInfo
        fields = ['order_id','user','total_count','total_amount','freight','pay_method','status','create_time','skus']


class OrderStatusModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderInfo
        fields = ['order_id','status']
