# Generated by Django 2.2 on 2020-01-29 16:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0003_blog_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='likes_on_comment',
            field=models.ManyToManyField(related_name='likes_on_comment', to=settings.AUTH_USER_MODEL),
        ),
    ]
