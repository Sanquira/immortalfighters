# Generated by Django 2.2 on 2019-06-23 07:56

from django.db import migrations

from dictionary.models import spell


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0017_auto_20190622_1930'),
    ]

    operations = [
        migrations.RunPython(spell.initialize_spell_directions),
    ]