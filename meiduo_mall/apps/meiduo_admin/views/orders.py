from rest_framework.generics import ListCreateAPIView,RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from apps.meiduo_admin.serializers.orders import OrdersModelSerializer, OrderDetailModelSerializer
from apps.meiduo_admin.utils import PageNum
from apps.orders.models import OrderInfo,OrderGoods


class OrdersListAPIView(ListCreateAPIView):
    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')
        if keyword:
            return OrderInfo.objects.filter(order_id__contains=keyword)
        else:
            return OrderInfo.objects.all()

    # 设置序列化器
    serializer_class = OrdersModelSerializer
    # 设置分页
    pagination_class = PageNum


class OrderDetailAPIView(RetrieveAPIView):
    queryset = OrderInfo.objects.all()
    serializer_class = OrderDetailModelSerializer
    lookup_field = 'order_id'
