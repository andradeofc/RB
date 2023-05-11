from django.urls import path
from django.conf import settings
from django.conf.urls.static import static, serve

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('admin/rule_update/', views.rule_create_or_update, name='rule-update'),
    path('admin/rule/', views.rule_detail, name='rule'),
    path('admin/', views.users_list, name='users-list'),
    path('admin/users/', views.users_list, name='users-list'),
    path('admin/user/<int:id>', views.user_detail, name='user-detail'),
    path('admin/user_update/<int:id>', views.user_update, name='user-update'),
    path('admin/user_delete/<int:id>', views.user_delete, name='user-delete'),
    path('admin/insert_users/', views.user_insert, name='user-insert'),
    path('admin/change_password/', views.password_change, name='password-change'),
    path('update_bank', views.bank_detail_update, name='bank-update'),
    path('login/', views.user_login, name='user-login'),
    path('insta/', views.instagram, name='insta'),
    path('youtube/', views.youtube, name='youtube'),
    path('tiktok/', views.tiktok, name='tiktok'),
    path('open_insta/', views.open_insta, name='open-insta'),
    path('open_youtube/', views.open_youtube, name='open-youtube'),
    path('open_tiktok/', views.open_tiktok, name='open-tiktok'),
    path('register/', views.register, name='register-user'),
    path('register_braip/', views.register_braip, name='register-user-braip'),
    path('register_orbita/', views.register_orbita, name='register-user-orbita'),
    path('register_perfectpay/', views.register_perfectpay, name='register-user-perfectpay'),
]