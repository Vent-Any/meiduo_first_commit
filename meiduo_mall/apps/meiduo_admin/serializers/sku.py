from apps.goods.models import SKU
from rest_framework import serializers


class SKUModelSerializer(serializers.ModelSerializer):
    # 对应外键值
    category_id = serializers.IntegerField()
    # 对应模型返回数值
    category = serializers.StringRelatedField()

    class Meta:
        model = SKU
        fields = '__all__'
