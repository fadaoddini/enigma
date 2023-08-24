from django.urls import path, re_path

from room.views import ChatApi, CategoryListApi, RoomApi, Text2img, TopicListApi, ListByUser, ListByUserTrue, TrueById

urlpatterns = [
    path('newchat', ChatApi.as_view(), name='chat'),
    path('newroom', RoomApi.as_view(), name='room'),
    path('text2img', Text2img.as_view(), name='text2img'),
    path('categorylist', CategoryListApi.as_view(), name='category-list'),
    path('topiclist', TopicListApi.as_view(), name='topic-list'),
    path('listbyuser', ListByUser.as_view(), name='listbyuser'),
    path('listbyusertrue', ListByUserTrue.as_view(), name='listbyusertrue'),
    path('truebyid', TrueById.as_view(), name='truebyid'),
]
