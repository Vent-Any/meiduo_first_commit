from apps.goods.models import SKUImage, SKU
from rest_framework import serializers

class SKUImageModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = SKUImage
        fields = '__all__'


class SimpleSKUModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = SKU
        fields = '__all__'