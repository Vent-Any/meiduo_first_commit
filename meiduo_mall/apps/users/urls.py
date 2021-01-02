from django.urls import path
from . import views

urlpatterns = [
    path('usernames/<uc:username>/count/', views.UsernameCountView.as_view()),
    path('mobiles/<mb:mobile>/count/', views.MobileCountView.as_view()),
    path('register/', views.RegisterView.as_view()),
]