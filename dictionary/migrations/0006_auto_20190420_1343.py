# Generated by Django 2.2 on 2019-04-20 11:43

from django.db import migrations

from dictionary.models import profession


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0005_auto_20190420_1303'),
    ]

    operations = [
        migrations.RunPython(profession.init_professions),
    ]
