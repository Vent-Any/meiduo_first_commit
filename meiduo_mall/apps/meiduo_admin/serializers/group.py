###################用户组####################################
from django.contrib.auth.models import Group, Permission
from rest_framework import serializers


class GroupModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'



class PermissionSimpleModelserializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'