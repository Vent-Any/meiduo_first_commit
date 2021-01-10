from django.urls import path
from . import views

urlpatterns = [
    # 用户名验证
    path('usernames/<uc:username>/count/', views.UsernameCountView.as_view()),
    # 手机号验证
    path('mobiles/<mb:mobile>/count/', views.MobileCountView.as_view()),
    # 用户注册
    path('register/', views.RegisterView.as_view()),
    # 用户登录
    path('login/', views.LoginView.as_view()),
    # 用户退出
    path('logout/', views.logoutView.as_view()),
    # 用户信息
    path('info/', views.UserInfoView.as_view()),
    # 邮件保存
    path('emails/', views.EmailView.as_view()),
    # 激活邮件
    path('emails/verification/', views.VerifyEmailView.as_view()),
    # 地址管理
    path('addresses/create/', views.CreateAddressView.as_view()),
    # 地址查询
    path('addresses/', views.AddressesListView.as_view()),
    # 用户浏览记录
    path('browse_histories/', views.UserHistoryView.as_view()),

]