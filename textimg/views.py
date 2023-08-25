import json
from random import randint

from django.shortcuts import render
from rest_framework.views import APIView

from mylogin.models import MyUser
from textimg import helper
from textimg.models import Textimg
from urllib import request as reqimg
from rest_framework.response import Response

from textimg.serializers import TextimgSerializer


class ChatImg(APIView):
    def post(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        user = body['user']
        chat = body['chat']
        user = MyUser.objects.get(pk=user)
        answer = helper.text2img(chat)
        image_url = answer["data"][0]["url"]
        Textimg.objects.create(
            user=user, link=image_url, chat=chat
        )
        data = {
            'link': image_url,
            'user': user.id,
            'chat': chat
        }
        return Response(data, content_type='application/json; charset=UTF-8')


class ListByUser(APIView):
    def post(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        user = body['user']
        user = MyUser.objects.filter(pk=user).first()
        textimg = Textimg.objects.filter(user=user).all()
        serializer = TextimgSerializer(textimg, many=True)
        return Response(serializer.data, content_type='application/json; charset=UTF-8')


class ListByUserTrue(APIView):
    def post(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        user = body['user']
        user = MyUser.objects.filter(pk=user).first()
        textimg = Textimg.objects.filter(user=user).filter(status=True).all()
        serializer = TextimgSerializer(textimg, many=True)
        return Response(serializer.data, content_type='application/json; charset=UTF-8')


class ListTrue(APIView):
    def post(self, request, *args, **kwargs):
        textimg = Textimg.objects.filter(status=True).all()
        serializer = TextimgSerializer(textimg, many=True)
        return Response(serializer.data, content_type='application/json; charset=UTF-8')


class TrueById(APIView):
    def post(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        id = body['id']
        textimg = Textimg.objects.get(pk=id)
        textimg.status = True
        textimg.save()
        serializer = TextimgSerializer(textimg)
        return Response(serializer.data, content_type='application/json; charset=UTF-8')