from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.meiduo_admin.login import admin_obtain_token
from apps.meiduo_admin.views import home, user, image, sku, orders,permission,group,admin

urlpatterns = [
    path('authorizations/', admin_obtain_token),
    # 日活用户统计
    path('statistical/day_active/', home.UserActiveAPIView.as_view()),
    # 日下单统计
    path('statistical/day_orders/', home.UserOrderAPIView.as_view()),
    # 日增用户统计
    path('statistical/day_increment/', home.DayUserAPIView.as_view()),
    # 月增用户统计
    path('statistical/month_increment/', home.MonthUserAPIView.as_view()),
    # 用户总量统计
    path('statistical/total_count/', home.TotalUserAPIView.as_view()),
    # 查询用户展示
    path('users/', user.UserListAPIView.as_view()),
    # SKU展示
    path('skus/simple/', image.SimpleSKUListAPIView.as_view()),
    # SKU的三级分类
    path('skus/categories/', sku.GoodCategoryAPIView.as_view()),
    # SPU简单获取
    path('goods/simple/', sku.SPUSimpleListView.as_view()),
    # 获取spu的规格和选项
    path('goods/<spu_id>/specs/', sku.GoodsSpecsAPIView.as_view()),
    # 订单信息展示
    path('orders/', orders.OrdersListAPIView.as_view()),
    # 订单详情展示
    path('orders/<pk>/', orders.OrderDetailAPIView.as_view()),
    # # 订单表状态修改
    path('orders/<pk>/status/', orders.OrderStatusAPIView.as_view()),
    # 权限管理
    path('permission/content_types/', permission.ContenTypeListAPIView.as_view()),
    # 获取组权限
    path('permission/simple/', group.PermissionSimpleModelView.as_view()),
    # 获取 分组表数据
    path('permission/groups/simple/', admin.GroupListAPIView.as_view()),
]
# 添加图片展示路由
# 创建router实例
router = DefaultRouter()
# 注册路由
router.register('skus/images', image.ImageModelViewSet, basename='images')
# 将路由添加到urlpatterns
urlpatterns += router.urls

# ＃＃＃SKU##### 展示SKU路由
router.register('skus', sku.SKUModelViewSet, basename='skus')
# 将路由添加到urlpatterns
urlpatterns += router.urls


# ##### Permission##### 权限管理
router.register('permission/perms', permission.PermissionModelViewSet, basename='perms')
# 将路由添加到urlpatterns
urlpatterns += router.urls

# ##### Group##### 组管理
router.register('permission/groups', group.GroupModelView, basename='groups')
# 将路由添加到urlpatterns
urlpatterns += router.urls

# ##### Admin##### 管理员管理
router.register('permission/admins', admin.AdminModelViewSet, basename='admins')
# 将路由添加到urlpatterns
urlpatterns += router.urls