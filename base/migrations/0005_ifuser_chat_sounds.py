# Generated by Django 2.2.7 on 2020-02-08 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_ifuser_chat_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='ifuser',
            name='chat_sounds',
            field=models.BooleanField(default=True, verbose_name='Zvuky chatu'),
        ),
    ]
