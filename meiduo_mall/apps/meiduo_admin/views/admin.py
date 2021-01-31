from django.contrib.auth.models import Group

from apps.meiduo_admin.serializers.admin import UserModelSerializer,GroupModelSerializer
from apps.meiduo_admin.utils import PageNum
from apps.users.models import User
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

class AdminModelViewSet(ModelViewSet):

    queryset = User.objects.filter(is_staff=1)
    serializer_class = UserModelSerializer
    pagination_class = PageNum


class GroupListAPIView(ListAPIView):

    queryset = Group.objects.all()
    serializer_class = GroupModelSerializer