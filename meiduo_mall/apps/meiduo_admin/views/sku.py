from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from apps.goods.models import SKU,GoodsCategory
from apps.meiduo_admin.serializers.sku import SKUModelSerializer,GoodsCategoryModelSerializer
from apps.meiduo_admin.utils import PageNum


class SKUModelViewSet(ModelViewSet):
    queryset = SKU.objects.all()
    serializer_class = SKUModelSerializer
    pagination_class = PageNum



class GoodCategoryAPIView(APIView):

    def get(self,request):
        gsc = GoodsCategory.objects.filter(subs=None)
        s =GoodsCategoryModelSerializer(instance=gsc,many=True)
        return Response(s.data)
