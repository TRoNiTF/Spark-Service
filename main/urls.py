from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('services/<int:service_id>/', views.service_detail, name='service_detail'),
    path('contacts/', views.contacts, name='contacts'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('call-request/', views.call_request, name='call_request'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
path('password-reset/', views.password_reset_request, name='password_reset_request'),
path('password-reset-confirm/<str:token>/', views.password_reset_confirm, name='password_reset_confirm'),
]

