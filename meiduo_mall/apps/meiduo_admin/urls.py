from django.urls import path
from apps.meiduo_admin.login import admin_obtain_token

urlpatterns = [
    path('authorizations/', admin_obtain_token),
]