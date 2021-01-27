from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.meiduo_admin.login import admin_obtain_token
from apps.meiduo_admin.views import home, user, image

urlpatterns = [
    path('authorizations/', admin_obtain_token),
    # 日活用户统计
    path('statistical/day_active/', home.UserActiveAPIView.as_view()),
    # 日下单统计
    path('statistical/day_orders/', home.UserOrderAPIView.as_view()),
    # 月增用户统计
    path('statistical/month_increment/', home.MonthUserAPIView.as_view()),
    # 查询用户展示
    path('users/', user.UserListAPIView.as_view()),
    # SKU展示
    path('skus/simple/', image.SimpleSKUListAPIView.as_view()),

]
# 添加图片展示路由
# 创建router实例
router = DefaultRouter()
# 注册路由
router.register('skus/images',image.ImageModelViewSet, basename='images')
# 将路由添加到urlpatterns
urlpatterns += router.urls