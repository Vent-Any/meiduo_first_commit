from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from apps.meiduo_admin.serializers.orders import OrdersModelSerializer, OrderDetailModelSerializer, \
    OrderStatusModelSerializer
from apps.meiduo_admin.utils import PageNum
from apps.orders.models import OrderInfo, OrderGoods


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


class OrderStatusAPIView(UpdateAPIView):
    queryset = OrderInfo.objects.all()
    serializer_class = OrderStatusModelSerializer

    def update(self, request, *args, **kwargs):

        order = OrderInfo.objects.get(order_id=kwargs.get('pk'))
        order.status = request.data.get('status')
        order.save()
        return Response({
            'order_id': order.order_id,
            'status': order.status
        })
