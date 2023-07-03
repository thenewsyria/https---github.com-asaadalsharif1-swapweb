from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from myapp.views import payment_gateway

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('send_otp/', views.send_otp, name='send_otp'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('categories/', views.get_categories, name='get_categories'),
    path('products/', views.get_products, name='get_products'),
    path('search_products/', views.search_products, name='search_products'),
        #http://localhost:8000/myapp/search_products/?query=music
    path('submit_support/', views.submit_support, name='submit_support'),
    path('historysupport/', views.historysupport, name='historysupport'),
    path('live_support/<int:support_id>/', views.live_support, name='live_support'),
    path('messages/', views.messages, name='messages'),
    path('payment_gateway/', payment_gateway, name='payment_gateway'),
    path('chat/', views.chat, name='chat'), # http://127.0.0.1:8000/myapp/chat/?other_user=Mohamed@gmail.com
    path('support/', views.create_support_ticket, name='create_support_ticket'),
    path('contracts/', views.contracts, name='contracts'),
     path('admin/password_reset/', auth_views.PasswordResetView.as_view(), name='admin_password_reset'),
    path('admin/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='admin_password_reset_done'),
    path('admin/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='admin_password_reset_confirm'),
    path('admin/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='admin_password_reset_complete'),
] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
