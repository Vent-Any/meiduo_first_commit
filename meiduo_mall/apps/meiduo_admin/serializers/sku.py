from apps.goods.models import SKU
from rest_framework import serializers


class SKUModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKU
        fields = '__all__'
