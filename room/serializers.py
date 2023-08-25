from rest_framework import serializers

from room.models import Category, Chat, Topic, Room


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


class RoomSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ('id', 'user', 'image', 'upc', 'name', 'status', 'create_time', 'category')

    def get_name(self, obj):
        name = obj.name
        name = name
        return name


class TopicSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = ('id', 'name', 'image', 'prompt')

    def get_name(self, obj):
        name = obj.name
        name = name
        return name


