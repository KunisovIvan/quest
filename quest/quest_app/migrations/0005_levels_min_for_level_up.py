# Generated by Django 4.0.2 on 2022-02-19 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quest_app', '0004_levels_min_for_hint1_levels_min_for_hint2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='levels',
            name='min_for_level_up',
            field=models.PositiveSmallIntegerField(default=60, verbose_name='Минут до конца уровня'),
        ),
    ]
