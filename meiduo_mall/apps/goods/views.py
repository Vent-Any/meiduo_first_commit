from django.core.paginator import EmptyPage, Paginator
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from collections import OrderedDict
from apps.goods.models import GoodsChannel, SKU, GoodsCategory
from utils.goods import get_breadcrumb


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