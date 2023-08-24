from django.contrib import admin
from django.contrib.admin import register

from room.models import Room, Category, Chat, Topic


@register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('user', 'upc', 'status')
    list_filter = ('status', )
    list_editable = ('status', )
    search_fields = ('upc', 'user')
    actions = ('active_all', 'deactive_all')

    def active_all(self, request, queryset):
        for queryone in queryset:
            room = Room.objects.filter(pk=queryone.pk).first()
            room.status = True
            room.save()

    def deactive_all(self, request, queryset):
            for queryone in queryset:
                room = Room.objects.filter(pk=queryone.pk).first()
                room.status = False
                room.save()


@register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)


@register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'prompt')
    search_fields = ('name', 'prompt')


@register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('chat', 'is_question')
    list_filter = ('is_question',)
    list_editable = ('is_question',)
    actions = ('active_all', 'deactive_all')

    def active_all(self, request, queryset):
        for queryone in queryset:
            chat = Chat.objects.filter(pk=queryone.pk).first()
            chat.is_question = True
            chat.save()

    def deactive_all(self, request, queryset):
        for queryone in queryset:
            room = Chat.objects.filter(pk=queryone.pk).first()
            room.is_question = False
            room.save()


