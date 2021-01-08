from django.urls import path
from . import views
urlpatterns = [
    path('oauth_callback/', views.QQUserView.as_view()),
]