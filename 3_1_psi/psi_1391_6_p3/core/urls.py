from django.urls import path
from core import views


app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('index/', views.home, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('convalidation/', views.convalidation, name='convalidation'),
    path('applypair/', views.apply_pair, name='applypair'),
    path('breakpair/', views.break_pair, name='breakpair'),
    path('applygroup/', views.apply_group, name='applygroup'),
]
