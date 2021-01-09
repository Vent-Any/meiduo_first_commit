from django.shortcuts import render

# Create your views here.
from django.views import View
from apps.areas.models import Area
from django.http.response import JsonResponse


class ProvienceView(View):
    def get(self, request):
        # 查询省份信息
        proviencs = Area.objects.filter(parent=None)
        # 将省份结果集转换为字典列表
        province_list = []
        for item in proviencs:
            province_list.append({
                'id': item.id,
                'name': item.name
            })
        # 返回响应
        return JsonResponse({'code': 0, 'errmsg': "OK", 'province_list': province_list})