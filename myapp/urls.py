from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('enter_otp/', views.enter_otp, name='enter_otp'),
    path('home/', views.home, name='home'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('search/', views.search, name='search'),
    path('category/<int:pk>/', views.category_products, name='category_products'),
    path('messages/', views.messages, name='messages'),
    path('chat/<int:other_user_id>/', views.chat, name='chat'),
    path('support/', views.support, name='support'),
    path('withdrawals/', views.withdrawals, name='withdrawals'),
    path('contracts/', views.contracts, name='contracts'),
]