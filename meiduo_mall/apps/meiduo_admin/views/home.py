from apps.users.models import User
from datetime import date
from rest_framework.views import APIView
from rest_framework.response import Response


# 日活用户统计
class UserActiveAPIView(APIView):
    def get(self,request):
        # 获取今天的时间
        today = date.today()
        # 过滤查询
        count = User.objects.filter(last_login__gte = today).count()
        # 返回响应
        return Response({'count':count})