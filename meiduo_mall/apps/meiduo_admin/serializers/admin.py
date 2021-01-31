from django.contrib.auth.models import Group

from apps.users.models import User
from rest_framework import serializers

class UserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        # 数据保存
        user = super().create(validated_data)
        # 密码加密
        user.set_password(validated_data.get('password'))
        # 设置普通管理员
        user.is_staff=True
        # 保存
        user.save()
        # 返回数据
        return user
class GroupModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'