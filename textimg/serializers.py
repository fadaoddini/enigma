from rest_framework import serializers

from room.models import Category, Chat, Topic
from textimg.models import Textimg


class TextimgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Textimg
        fields = ('id', 'chat', 'user', 'link', 'status')
