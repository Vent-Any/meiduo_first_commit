from rest_framework.generics import ListCreateAPIView
from apps.meiduo_admin.utils import PageNum
from apps.users.models import User
from apps.meiduo_admin.serializers.user import UserModelSerializer

class UserListAPIView(ListCreateAPIView):
    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')
        if keyword:
            return User.objects.filter(username__contains=keyword)
        else:
            return User.objects.all()
    # 设置序列化器
    serializer_class = UserModelSerializer
    # 设置分页
    pagination_class = PageNum




