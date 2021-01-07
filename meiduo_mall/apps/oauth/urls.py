from django.urls import path
from . import views
urlpatterns = [
    path('oauth_callback/', views.QQAuthUserView.as_view()),
]