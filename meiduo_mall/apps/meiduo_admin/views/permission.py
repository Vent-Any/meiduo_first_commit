from django.contrib.auth.models import Permission,ContentType

from rest_framework.viewsets import ModelViewSet
from apps.meiduo_admin.serializers.permission import PermissionModelSerializer
from apps.meiduo_admin.utils import PageNum

class PermissionModelViewSet(ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionModelSerializer
    pagination_class = PageNum



#########################权限的内容类型#######################

from django.contrib.auth.models import ContentType
from rest_framework.generics import ListAPIView
from apps.meiduo_admin.serializers.permission import  ContentTypeModelSerializer

class ContenTypeListAPIView(ListAPIView):
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeModelSerializer