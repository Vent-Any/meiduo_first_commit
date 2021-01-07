from django.urls import path
from . import views
urlpatterns = [
    path('image_codes/<uuid:uuid>/', views.ImageCodeView.as_view()),
    path('sms_codes/<mobile>/', views.SMSCodeView.as_view()),

]