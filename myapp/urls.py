from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from myapp.views import payment_gateway

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('terms_and_conditions/', views.terms_and_conditions, name='terms_and_conditions'),
    #http://localhost:8000/myapp/social-login/google/
    path('social-login/<backend>/', views.social_login, name='social-login'),
    path('social-sign-up/<backend>/', views.social_sign_up, name='social-sign-up'),
#http://127.0.0.1:8000/api/social-login/google/
    path('send_otp/', views.send_otp, name='send_otp'),
   
    path('categories/', views.get_categories, name='get_categories'),
    path('products/', views.get_products, name='get_products'),
    path('get_all_products/', views.get_all_products, name='get_all_products'),
    path('upload_product/', views.upload_product, name='upload_product'),
    path('add-favorite/<int:product_id>/', views.addProductToFavorit, name='add_product_to_favorit'),
    path('get_profile/', views.get_profile , name='get_profile'),
    path('edit_profile/', views.edit_profile , name='edit_profile'),
    path('search_products/', views.search_products, name='search_products'),
        #http://localhost:8000/myapp/search_products/?query=music
    path('submit_support/', views.submit_support, name='submit_support'),
    path('historysupport/', views.historysupport, name='historysupport'),
    path('live_support/<int:support_id>/', views.live_support, name='live_support'),
    path('payment_gateway/', payment_gateway, name='payment_gateway'),
    path('chat/<product_id>/', views.chat, name='chat'), 
    path('get_messages/<product_id>/', views.get_messages, name='get_messages'), 
    path('contracts/', views.contracts, name='contracts'),
     path('admin/password_reset/', auth_views.PasswordResetView.as_view(), name='admin_password_reset'),
    path('admin/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='admin_password_reset_done'),
    path('admin/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='admin_password_reset_confirm'),
    path('admin/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='admin_password_reset_complete'),
] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
