"""weather URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path

from mainapp.views import (
    login_view, logout_view, signup_view, profile_view, edit_profile_view, users_list_view
)

from mainapp.api import hobbies_api, profile_api, users_api, sent_friend_request_api, received_friend_request_api, friend_api

urlpatterns = [
    path('', profile_view, name='profile'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
	path('edit-profile/', edit_profile_view, name='edit_profile'),
	path('users/', users_list_view, name='users_list'),

    path('api/hobbies/', hobbies_api, name="hobbies api"),
    path('api/profile/', profile_api, name="profile api"),
    path('api/users/', users_api, name="users api"),
    path('api/sent_friend_request_api/', sent_friend_request_api, name="sent request api"),
    path('api/received_friend_request_api/', received_friend_request_api, name="received request api"),
    path('api/friend_api/', friend_api, name="friend api"),
]
