# Generated by Django 2.2 on 2019-04-19 10:22

from django.db import migrations

from dictionary.models import race


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(race.initialize_races),
    ]