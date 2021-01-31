from django.contrib.auth.models import Permission,ContentType
from rest_framework import serializers

class PermissionModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = '__all__'



class ContentTypeModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContentType
        fields = ['id','name']