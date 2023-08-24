from django.urls import path, re_path

from textimg.views import ChatImg, ListByUser, ListByUserTrue, TrueById

urlpatterns = [
    path('chatimg', ChatImg.as_view(), name='chatimg'),
    path('listbyuser', ListByUser.as_view(), name='listbyuser'),
    path('listbyusertrue', ListByUserTrue.as_view(), name='listbyusertrue'),
    path('truebyid', TrueById.as_view(), name='truebyid'),
]
