
######################################用户组######################################
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import Group, Permission
from apps.meiduo_admin.utils import PageNum

from apps.meiduo_admin.serializers.group import GroupModelSerializer,PermissionSimpleModelserializer


class GroupModelView(ModelViewSet):
    queryset =Group.objects.all()
    serializer_class = GroupModelSerializer
    pagination_class = PageNum


class PermissionSimpleModelView(ListAPIView):
    queryset =Permission.objects.all()
    serializer_class =PermissionSimpleModelserializer
