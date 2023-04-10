"""ebooking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from hotels.views import *
from django.conf import settings
from django.conf.urls.static import static
from reservation.views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', index, name="home"), 
    path('home', index, name="home"), 
    
    path('hotel_rooms/<int:hotel_id>/', edit_rooms_view, name="admin_hotel_rooms"), # Hotel Administrator
    
    path('rooms/<int:hotel_id>/', hotel_rooms_view, name="user_hotel_rooms"),
    path('rooms/edit/<int:hotel_id>/<int:room_id>/', edit_room_view, name='edit_room'),
    path('rooms/add/<int:hotel_id>/', add_room_view, name='add_room'), # Hotel Administrator
    path('rooms/delete/<int:hotel_id>/<int:room_id>/', delete_room_view, name='delete_room'), # Hotel Administrator
    path('reservation/', include('reservation.urls')),
    path('accounts/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
