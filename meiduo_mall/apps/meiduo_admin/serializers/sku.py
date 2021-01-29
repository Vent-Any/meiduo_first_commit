from apps.goods.models import SKU, GoodsCategory, SPU
from rest_framework import serializers


class SKUModelSerializer(serializers.ModelSerializer):
    # 对应外键值
    category_id = serializers.IntegerField()
    # 对应模型返回数值
    category = serializers.StringRelatedField()

    class Meta:
        model = SKU
        fields = '__all__'


class GoodsCategoryModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = GoodsCategory
        fields = ['id','name']



class SPUSimpleModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = SPU
        fields = ['id','name']
