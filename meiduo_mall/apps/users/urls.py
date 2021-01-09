from django.urls import path
from . import views

urlpatterns = [
    path('usernames/<uc:username>/count/', views.UsernameCountView.as_view()),
    path('mobiles/<mb:mobile>/count/', views.MobileCountView.as_view()),
    path('register/', views.RegisterView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.logoutView.as_view()),
    path('info/', views.UserInfoView.as_view()),
    path('emails/', views.EmailView.as_view()),
    path('emails/verification/', views.VerifyEmailView.as_view()),
]