from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('auth/login/', views.UserAuthView.as_view(), name='user_auth'),
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('logout/', views.LogoutView.as_view(), name='user_logout'),
]
