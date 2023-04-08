from django.urls import path
from django.contrib.auth import views as auth_views
from .views import MyLoginView, register


app_name = 'accounts'

urlpatterns = [
    path('log-in/', MyLoginView.as_view(), name='log_in'),
    path('log-out/', auth_views.LogoutView.as_view(), name='log_out'),
    path('register/', register, name='register'),
]