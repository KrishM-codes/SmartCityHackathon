from django.contrib import admin
from django.urls import include, path
from . import views
urlpatterns = [
    path('', view=views.home,name = 'home'),
    path('queries', view=views.queries,name = 'queries'),
    path('register', view=views.registerUser,name = 'register'),
    path('login', view=views.loginUser,name = 'login'),
    path('dashboard',view=views.dashboard,name='dashboard'),
    path('postquery',view=views.postQuery,name='postquery')
]