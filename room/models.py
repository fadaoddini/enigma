import random

from django.db import models, transaction
from django.contrib.auth import get_user_model as user_model
# Create your models here.


class Category(models.Model):
    ACTIVE = True
    INACTIVE = False
    STATUS_TYPE = (
        (ACTIVE, 'True'),
        (INACTIVE, 'False')
    )
    name = models.CharField(max_length=32)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)
    image = models.ImageField(upload_to='%Y/%m/%d/img-category/', null=True, blank=True)
    status = models.BooleanField(choices=STATUS_TYPE, default=ACTIVE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Room(models.Model):

    ACTIVE = True
    INACTIVE = False

    STATUS_ROOM = (
        (ACTIVE, 'true'),
        (INACTIVE, 'false'),
    )
    User = user_model()
    user = models.ForeignKey(User, related_name='rooms', on_delete=models.RESTRICT)
    image = models.ImageField(upload_to='%Y/%m/%d/img-room/', null=True, blank=True)
    category = models.ForeignKey(Category, related_name='categoryrooms', on_delete=models.PROTECT)
    upc = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=42)
    status = models.BooleanField(choices=STATUS_ROOM, default=INACTIVE)
    create_time = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Room'
        verbose_name_plural = "Rooms"

    def __str__(self):
        return self.name

    @classmethod
    def add_room(cls, request):
        result = "200"
        is_active = False
        upc = random.randint(1111111111111111111, 9999999999999999999)
        form = request.POST
        user = request.user
        category = form.get('category')
        if category != "None":
            pass
        else:
            result = "40"
            return result

        name = form.get('name')

        new_product = Room(user=user, category=category, upc=upc,
                                name=name)
        new_product.save()
        return result


class Chat(models.Model):

    chat = models.TextField(blank=True)
    room = models.ForeignKey(Room, related_name='chats', on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Chat'
        verbose_name_plural = 'Chats'

    def __str__(self):
        return self.chat

