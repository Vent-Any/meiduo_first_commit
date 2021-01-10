from django.core.paginator import EmptyPage, Paginator
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from collections import OrderedDict
from apps.goods.models import GoodsChannel, SKU, GoodsCategory
from utils import models
from utils.goods import get_breadcrumb, get_categories, get_goods_specs


class IndexView(View):
    """首页广告"""

    def get(self, request):
        """提供首页广告界面"""
        # 查询商品频道和分类
        categories = OrderedDict()
        channels = GoodsChannel.objects.order_by('group_id', 'sequence')
        for channel in channels:
            group_id = channel.group_id  # 当前组

            if group_id not in categories:
                categories[group_id] = {'channels': [], 'sub_cats': []}

            cat1 = channel.category  # 当前频道的类别

            # 追加当前频道
            categories[group_id]['channels'].append({
                'id': cat1.id,
                'name': cat1.name,
                'url': channel.url
            })
            # 构建当前类别的子类别
            for cat2 in cat1.subs.all():
                cat2.sub_cats = []
                for cat3 in cat2.subs.all():
                    cat2.sub_cats.append(cat3)
                categories[group_id]['sub_cats'].append(cat2)
        return categories

class ListView(View):
    """商品列表页"""

    def get(self, request, category_id):
        """提供商品列表页"""
        # 获取参数:
        page = request.GET.get('page')
        page_size = request.GET.get('page_size')
        ordering = request.GET.get('ordering')

        # 判断category_id是否正确
        try:
            # 获取三级菜单分类信息:
            category = GoodsCategory.objects.get(id=category_id)
        except Exception as e:
            return JsonResponse({'code':400,
                                 'errmsg':'获取mysql数据出错'})

        # 查询面包屑导航(函数在下面写着)
        breadcrumb = get_breadcrumb(category)

        # 排序方式:
        try:
            skus = SKU.objects.filter(category=category,
                                      is_launched=True).order_by(ordering)
        except Exception as e:
            return JsonResponse({'code':400,
                                 'errmsg':'获取mysql数据出错'})

        paginator = Paginator(skus, page_size)
        # 获取每页商品数据
        try:
            page_skus = paginator.page(page)
        except EmptyPage:
            # 如果page_num不正确，默认给用户400
            return JsonResponse({'code':400,
                                 'errmsg':'page数据出错'})
        # 获取列表页总页数
        total_page = paginator.num_pages

        # 定义列表:
        list = []
        # 整理格式:
        for sku in page_skus:
            list.append({
                'id':sku.id,
                'default_image_url':sku.default_image.url,
                'name':sku.name,
                'price':sku.price
            })

        # 把数据变为 json 发送给前端
        return JsonResponse({
                             'code':0,
                             'errmsg':'ok',
                             'breadcrumb': breadcrumb,
                             'list':list,
                             'count':total_page
                            })

class HotView(View):
    """商品热销排行"""

    def get(self, request, category_id):
        """提供商品热销排行JSON数据"""
        # 根据销量倒序
        skus = SKU.objects.filter(category_id=category_id, is_launched=True).order_by('-sales')[:2]

        # 序列化
        hot_skus = []
        for sku in skus:
            hot_skus.append({
                'id':sku.id,
                'default_image_url':sku.default_image.url,
                'name':sku.name,
                'price':sku.price
            })

        return JsonResponse({'code':0, 'errmsg':'OK', 'hot_skus':hot_skus})

from utils.goods import get_breadcrumb,get_categories,get_goods_specs
class DetailView(View):
    def get(self,request,sku_id):
        """
        1. 获取商品id
        2. 根据商品id查询商品信息
        3. 获取分类数据
        4. 获取面包屑数据
        5. 获取规格和规格选项数据
        6. 组织数据,进行HTML模板渲染
        7. 返回响应
        :param request:
        :param sku_id:
        :return:
        """
        # 1. 获取商品id
        # 2. 根据商品id查询商品信息
        try:
            sku=SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return JsonResponse({'code':400,'errmsg':'没有此商品'})
        # 3. 获取分类数据
        categories = get_categories()
        # 4. 获取面包屑数据
        # sku 有 三级分类属性
        breadcrumb=get_breadcrumb(sku.category)
        # 5. 获取规格和规格选项数据
        # 传递 sku对象
        specs = get_goods_specs(sku)
        # 6. 组织数据,进行HTML模板渲染
        # context 的key 必须按照课件来!!!
        # 因为模板已经写死了
        context = {
        'sku':sku,
        'categories':categories,
        'breadcrumb':breadcrumb,
        'specs':specs
        }
        # 7. 返回响应
        return render(request,'detail.html',context)


from apps.goods.models import GoodsVisitCount
class CategoryVisitView(View):
    def post(self,request,category_id):
        """
        1. 获取分类id
        2. 根据分类id查询分类数据
        3. 获取当天日期
        4. 我们要查询数据库,是否存在 分类和日期 的记录
        5. 如果不存在 则新增记录
        6. 如果存在,则修改count
        7. 返回响应
        :param request:
        :param category_id:
        :return:
        """
        # 1. 获取分类id
        # 2. 根据分类id查询分类数据
        try:
            category=GoodsCategory.objects.get(id=category_id)
        except GoodsCategory.DoesNotExist:
            return JsonResponse({"code":0,'errmsg':'没有次分类'})
        # 3. 获取当天日期
        from datetime import date
        today=date.today()
        # 4. 我们要查询数据库,是否存在 分类和日期 的记录
        try:
            gvc=GoodsVisitCount.objects.get(category=category,date=today)
        except GoodsVisitCount.DoesNotExist:
            # 5. 如果不存在 则新增记录
            GoodsVisitCount.objects.create(
            category=category,
            date=today,
            count=1
            )
        else:
            # 6. 如果存在,则修改count
            gvc.count += 1
            gvc.save()
            # 7. 返回响应
            return JsonResponse({"code":0,"errmsg":'ok'})