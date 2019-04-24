# Generated by Django 2.2 on 2019-04-24 20:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_character_profession'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='character',
            options={'verbose_name': 'Postava', 'verbose_name_plural': 'Postavy'},
        ),
        migrations.AlterModelOptions(
            name='ifuser',
            options={'verbose_name': 'Uživatel', 'verbose_name_plural': 'Uživatelé'},
        ),
        migrations.RemoveField(
            model_name='character',
            name='experience_points',
        ),
        migrations.RemoveField(
            model_name='character',
            name='level',
        ),
        migrations.RemoveField(
            model_name='character',
            name='stat_charisma',
        ),
        migrations.RemoveField(
            model_name='character',
            name='stat_dexterity',
        ),
        migrations.RemoveField(
            model_name='character',
            name='stat_intelligence',
        ),
        migrations.RemoveField(
            model_name='character',
            name='stat_resistance',
        ),
        migrations.RemoveField(
            model_name='character',
            name='stat_strength',
        ),
        migrations.AlterField(
            model_name='character',
            name='character_name',
            field=models.CharField(max_length=50, null=True, verbose_name='Jméno postavy'),
        ),
        migrations.AlterField(
            model_name='character',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Vlastník'),
        ),
        migrations.AlterField(
            model_name='character',
            name='profession',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dictionary.BaseProfession', verbose_name='Povolání'),
        ),
        migrations.AlterField(
            model_name='character',
            name='race',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dictionary.Race', verbose_name='Rasa'),
        ),
        migrations.AlterField(
            model_name='ifuser',
            name='active_char',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.Character', verbose_name='Aktivní postava'),
        ),
    ]
