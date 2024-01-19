from django.urls import path, include
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.index, name='index'),
    path('group_list/<slug:slug>/', views.group_posts, name='group_list'),
]