# Generated by Django 4.2.4 on 2023-08-24 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0002_room_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='is_question',
            field=models.BooleanField(choices=[(True, 'true'), (False, 'false')], default=1),
            preserve_default=False,
        ),
    ]
