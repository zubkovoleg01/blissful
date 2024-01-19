from django.urls import path, include
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.index, name='index'),
    path('group_list/', views.group_list, name='group_list'),
    path('post/<str:pk>/', views.post_detail, name='post_detail'),
]