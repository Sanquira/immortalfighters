# Generated by Django 2.2.10 on 2020-02-27 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_historyrecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='permission',
            field=models.CharField(blank=True, default=None, max_length=30, null=True),
        ),
    ]