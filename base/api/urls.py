from django.urls import path
from . import views
from .views import MyTokenObtainPairView
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('', views.getRoutes),
    path('register/', views.register, name='register'),
    path('getCsrf/', views.getCsrf, name='getCsrf'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('user_view/', views.user_view, name='user_view'),
    path('user_list/', views.user_list, name='user_list'),
    path('user_create/', views.user_create, name='user_create'),
    path('user_crud/<int:user_id>/', views.user_crud, name='user_crud'),

    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

] 

# admin@gmail.com