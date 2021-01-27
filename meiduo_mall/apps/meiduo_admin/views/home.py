from apps.users.models import User
from datetime import date, timedelta
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

# 下单用户
class UserOrderAPIView(APIView):
    def get(self,request):
        today = date.today()
        count = User.objects.filter(orderinfo__create_time__gte=today).count()
        return Response({'count':count})


# 统计月增用户
class MonthUserAPIView(APIView):
    def get(self,request):
        today = date.today()
        before_day = today - timedelta(days=30)
        data_list = []
        for i in range(0,30):
            start_date = before_day + timedelta(days=i)
            end_date = before_day + timedelta(days=(i+1))
            count =User.objects.filter(date_joined__gte=start_date, date_joined__lt=end_date).count()
            data_list.append({
                'count':count,
                'date':start_date
            })
        return Response(data_list)