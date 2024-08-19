from django.contrib import admin
from django.urls import path
from . import views
from .auth import CustomAuthToken
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('home', view=views.home,name = 'home'),
    # path('queries', view=views.queries,name = 'queries'),
    path('queryapiview',view=views.QueryAPI.as_view(),name='queryapiview'),
    path('queryapiview/<int:pk>',view=views.QueryAPI.as_view(),name='queryapiview'),
    path('register', view=views.registerUser,name = 'register'),
    path('login', view=views.loginUser,name = 'login'),
    path('dashboard',view=views.dashboard,name='dashboard'),
    path('postquery',view=views.postQuery,name='postquery'),
    path('gettoken',CustomAuthToken.as_view()),
]