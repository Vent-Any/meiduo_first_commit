from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from apps.goods.models import SKU

from apps.goods.models import SKUImage
from apps.meiduo_admin.serializers.image import SKUImageModelSerializer,SimpleSKUModelSerializer
from apps.meiduo_admin.utils import PageNum


class  ImageModelViewSet(ModelViewSet):
    # 设置查询结果集
    queryset = SKUImage.objects.all()
    # 序列化器
    serializer_class = SKUImageModelSerializer
    # 分页
    pagination_class = PageNum


class SimpleSKUListAPIView(ListAPIView):
    queryset = SKU.objects.all()
    serializer_class = SimpleSKUModelSerializer



# 新增图片
class ImageModelView(ModelViewSet):
    queryset = SKUImage.objects.all()
    serializer_class = SKUImageModelSerializer
    pagination_class = PageNum
    def create(self, request, *args, **kwargs):
        upload_image = request.FILES.get('image')
        data = request.data
        sku_id = data.get('sku')
        try:
            sku = SKU.objects.get(id=sku_id)
        except:
            return Response({'msg':'没有此商品'})
        from qiniu import Auth,put_data,etag
        # 秘钥
        access_key = 'q9crPZPROOXrykaH85q_zpEEll0f_LsjXwUnXHRo'
        secret_key = 'lG_4_tI8bJTR8Zk6z8fGwYp79aQHkJgolvvBL_qm'
        # 创建鉴权对象
        q =Auth(access_key,secret_key)
        # 要上传的空间
        bucket_name = 'shunyi44'
        # 上传保存文件名__使用系统
        key=None
        # 生成上传Token,可以指定过期时间
        token = q.upload_token(bucket_name,key,3600)
        # 获取上传图片的二进制
        data = upload_image.read()
        # ret 结果
        ret , info = put_data(token,key,data=data)
        # 自动生成的图片名字
        image_url = ret['key']
        # 数据入库
        new_image =SKUImage.objects.create(
            sku_id=sku_id,
            image = image_url
        )
        return Response({
            'id':new_image.id,
            'image':new_image.image.url,
            'sku':sku_id
        },status=201)