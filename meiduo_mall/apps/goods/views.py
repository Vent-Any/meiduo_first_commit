from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render
from apps.goods.models import GoodsCategory, SKU
# Create your views here.
from django.views import View

from utils.goods import *


class IndexView(View):

    def get(self, request):
        """
        1. 获取分类数据
        2. 获取首页数据
        3. 组织数据 进行渲染
        :param request:
        :return:
        """
        # 1. 获取分类数据
        categories = get_categories()
        # 2. 获取首页数据
        contents = get_contents()
        # 3. 组织数据 进行渲染
        # 注意: key必须是这2个 因为模板中已经写死
        context = {
            'categories': categories,
            'contents': contents
        }
        return render(request, 'index.html', context)