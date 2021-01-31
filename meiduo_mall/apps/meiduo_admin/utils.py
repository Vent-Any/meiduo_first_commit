from rest_framework.response import Response


def jwt_response_playload_handler(token, user=None, request=None):
    return {
            'token': token,
            'username':user.username,
            'user_id':user.id
            }

# 定义分页类
from rest_framework.pagination import PageNumberPagination
class  PageNum(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'pagesize'

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,  # 总共有多少条记录
            'lists': data,  # 数据
            'page': self.page.number,  # 第几页
            'pages': self.page.paginator.num_pages,  # 总共多少页
            'pagesize': self.page_size,  # 每页多少条数据
        })