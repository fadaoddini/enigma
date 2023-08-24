from django.shortcuts import render
from rest_framework.views import APIView
import json
from mylogin.models import MyUser
from rest_framework.response import Response

from room import helper
from room.models import Room, Category, Chat
from room.serializers import CategorySerializer, ChatListInRoomSerializer


class ChatApi(APIView):
    def post(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        chat = body['chat']
        roomid = body['room']
        room = Room.objects.filter(pk=roomid)
        if room.exists():
            chat_list = dict()
            print("before room")
            messege = "روم از قبل وجود داشت، می توانید گفتگوی خود را ادامه دهید..."
            room = room.first()
            user = room.user
            print(user)
            # just add chat
            is_question = True
            Chat.objects.create(
                chat=chat, is_question=is_question, room=room
            )
            status_result = "ok"
            answer = helper.robot(chat)
            result = answer['choices'][0]['message']['content']
            Chat.objects.create(
                chat=result, is_question=False, room=room
            )
            allchat = Chat.objects.filter(room=room).all()
            serializerallchat = ChatListInRoomSerializer(allchat, many=True)

        else:
            status_result = "no"
        data = {
            'allchatinroom': serializerallchat.data,
            'status': status_result
        }
        return Response(data, content_type='application/json; charset=UTF-8')


class RoomApi(APIView):
    def post(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        upc = helper.create_random_upc()
        user = body['user']
        category = body['category']
        chat = body['chat']
        # get category
        category = Category.objects.filter(pk=category).first()
        user = MyUser.objects.get(pk=user)
        status = False
        room = Room.objects.create(
            user=user, category=category, upc=upc, name=chat, status=status
        )
        Chat.objects.create(
            chat=chat, is_question=True, room=room
        )
        answer = helper.robot(chat)
        result = answer['choices'][0]['message']['content']
        Chat.objects.create(
            chat=result, is_question=False, room=room
        )
        allchat = Chat.objects.filter(room=room).all()
        serializerallchat = ChatListInRoomSerializer(allchat, many=True)
        status_result = "ok"
        data = {
            'allchatinroom': serializerallchat.data,
            'status': status_result
        }
        return Response(data, content_type='application/json; charset=UTF-8')


class CategoryListApi(APIView):
    def get(self, request, *args, **kwargs):
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data, content_type='application/json; charset=UTF-8')


class Text2img(APIView):
    def post(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        chat = body['chat']
        answer = helper.text2img(chat)
        # result = answer['choices'][0]['message']['content']
        data = {
            'link': answer
        }
        return Response(data, content_type='application/json; charset=UTF-8')
