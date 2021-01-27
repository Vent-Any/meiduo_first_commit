from django.urls import path
from apps.meiduo_admin.login import admin_obtain_token
from apps.meiduo_admin.views import home

urlpatterns = [
    path('authorizations/', admin_obtain_token),
    # 日活用户统计
    path('statistical/day_active/', home.UserActiveAPIView.as_view()),
    path('statistical/day_orders/', home.UserOrderAPIView.as_view()),

]