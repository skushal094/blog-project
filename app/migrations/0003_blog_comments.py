# Generated by Django 2.2.9 on 2020-01-09 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_blog_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='comments',
            field=models.IntegerField(default=0),
        ),
    ]
