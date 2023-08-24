from django.urls import path, re_path

from room.views import ChatApi, CategoryListApi, RoomApi

urlpatterns = [
    path('newchat', ChatApi.as_view(), name='chat'),
    path('newroom', RoomApi.as_view(), name='room'),
    path('categorylist', CategoryListApi.as_view(), name='category-list'),
]
