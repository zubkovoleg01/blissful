from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('post/', views.post),
    path(
        'post/<str:pk>/',
        views.post_detail
    ),
]