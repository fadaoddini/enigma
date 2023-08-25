from django.contrib import admin
from django.contrib.admin import register

from textimg.models import Textimg


@register(Textimg)
class TextimgAdmin(admin.ModelAdmin):
    list_display = ('chat', 'link', 'user', 'status')

