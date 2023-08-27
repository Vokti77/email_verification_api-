
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('activate/<str:uidb64>/<str:token>/', views.activate_user, name='activate'),
    path('change-password/', views.change_password, name='change-password'),
    path('request-password-reset/', views.request_password_reset, name='request-password-reset'),
    path('user-information/', views.user_information, name='user-information'),
]














