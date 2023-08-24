from django.db import models
from django.contrib.auth import get_user_model as user_model


class Textimg(models.Model):
    ACTIVE = True
    INACTIVE = False
    STATUS_TYPE = (
        (ACTIVE, 'True'),
        (INACTIVE, 'False')
    )
    chat = models.TextField(blank=True)
    link = models.TextField(blank=True)
    User = user_model()
    user = models.ForeignKey(User, related_name='textimgs', on_delete=models.RESTRICT)
    status = models.BooleanField(choices=STATUS_TYPE, default=INACTIVE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Textimg'
        verbose_name_plural = 'Textimgs'

    def __str__(self):
        return self.chat

