from django.urls import path, re_path

from room.views import ChatApi, CategoryListApi, RoomApi, Text2img

urlpatterns = [
    path('newchat', ChatApi.as_view(), name='chat'),
    path('newroom', RoomApi.as_view(), name='room'),
    path('text2img', Text2img.as_view(), name='text2img'),
    path('categorylist', CategoryListApi.as_view(), name='category-list'),
]
