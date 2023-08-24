from rest_framework import serializers

from room.models import Category, Chat


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'image')

    def get_name(self, obj):
        name = obj.name
        name = name
        return name


class ChatListInRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ('id', 'chat', 'room', 'is_question')

