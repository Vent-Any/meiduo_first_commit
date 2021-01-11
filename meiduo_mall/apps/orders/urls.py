from django.urls import path
from apps.orders.views import OrderSubmitView
urlpatterns = [
    path('orders/settlement/', OrderSubmitView.as_view()),
]