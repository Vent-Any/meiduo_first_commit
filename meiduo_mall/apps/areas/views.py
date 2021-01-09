from django.shortcuts import render

# Create your views here.
from django.views import View
from apps.areas.models import Area
from django.http.response import JsonResponse
from django.core.cache import cache


class ProvienceView(View):
    def get(self, request):
        # 判断缓存是否存在
        province_list = cache.get('province')
        if province_list is None:
            # 查询省份信息
            proviencs = Area.objects.filter(parent=None)
            # 将省份结果集转换为字典列表
            province_list = []
            for item in proviencs:
                province_list.append({
                    'id': item.id,
                    'name': item.name
                })
        # 将数据进行缓存
        cache.set('province', province_list, 24*3600)
        # 返回响应
        return JsonResponse({'code': 0, 'errmsg': "OK", 'province_list': province_list})

class SubAreaView(View):
    def get(self, request, pk):
        # 接受参数
        # 进行数据的判断(是否在缓存中)
        sub_list = cache.get('sub_area_%s' % pk)
        if sub_list is None:
            # 1. 接收参数 因为前端传递的 上一级id 在url中,所以我们在url中已经获取到了 上一级id
            # pk 就是 parent_id
            # 2. 根据 parent_id 进行查询
            sub_areas = Area.objects.filter(parent_id=pk)
            sub_list = []
            for item in sub_areas:
                sub_list.append({
                    'id':item.id,
                    'name':item.name
                })
        # 将数据进行缓存
        cache.set('sub_area_%s'%pk,sub_list,24*3600)
        # 返回数据
        return JsonResponse({'code': 0, 'errmsg':"OK", 'sub_data': {'subs': sub_list}})