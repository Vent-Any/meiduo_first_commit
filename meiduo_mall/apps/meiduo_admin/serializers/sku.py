from apps.goods.models import SKU, GoodsCategory, SPU, SPUSpecification, SKUSpecification
from rest_framework import serializers


class SKUSpecificationModelSerializer(serializers.ModelSerializer):
    spec_id = serializers.IntegerField()
    option_id = serializers.IntegerField()

    class Meta:
        model = SKUSpecification
        fields = ['spec_id', 'option_id']


class SKUModelSerializer(serializers.ModelSerializer):
    # 对应外键值
    category_id = serializers.IntegerField()
    # 对应模型返回数值
    category = serializers.StringRelatedField()

    spu = serializers.StringRelatedField()
    spu_id = serializers.IntegerField()

    specs = SKUSpecificationModelSerializer(many=True)

    class Meta:
        model = SKU
        fields = '__all__'

    def create(self, validated_data):
        specs = validated_data.pop('specs')
        from django.db import transaction
        with transaction.atomic():
            save_point = transaction.savepoint()
            try:
                sku = SKU.objects.create(**validated_data)
                for spec in specs:
                    SKUSpecification.objects.create(sku=sku, **spec)
            except:
                transaction.savepoint_rollback(save_point)

            else:
                transaction.savepoint_commit(save_point)
        return sku

    def update(self, instance, validated_data):
        specs = validated_data.pop('specs')
        super().update(instance,validated_data)
        for spec in specs:
            SKUSpecification.objects.filter(sku=instance,spec_id=spec.get('spec_id')).update(option_id=spec.get('option_id'))

        return instance


class GoodsCategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = ['id', 'name']


class SPUSimpleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SPU
        fields = ['id', 'name']


from apps.goods.models import SpecificationOption


class SpecificationOptionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecificationOption
        fields = ['id', 'value']


class SPUSpecsModelSerializer(serializers.ModelSerializer):
    spu = serializers.StringRelatedField()
    spu_id = serializers.IntegerField()
    options = SpecificationOptionModelSerializer(many=True)

    class Meta:
        model = SPUSpecification
        fields = ['id', 'name', 'spu', 'spu_id', 'options']
