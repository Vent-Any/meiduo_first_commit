from django.urls import path
from apps.areas.views import *
urlpatterns = [
    path('areas/', ProvienceView.as_view()),
    path('areas/<pk>/', SubAreaView.as_view()),
]