# Generated by Django 2.2 on 2020-01-29 16:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_comment_likes_on_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='likes_on_comment',
            field=models.ManyToManyField(blank=True, related_name='likes_on_comment', to=settings.AUTH_USER_MODEL),
        ),
    ]
