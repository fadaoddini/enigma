# Generated by Django 4.2.4 on 2023-08-25 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('textimg', '0002_remove_textimg_image_textimg_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='textimg',
            name='status',
            field=models.BooleanField(choices=[(True, 'True'), (False, 'False')], default=False),
        ),
    ]