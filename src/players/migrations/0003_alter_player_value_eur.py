# Generated by Django 4.0.1 on 2022-04-02 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0002_alter_player_attacking_crossing_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='value_eur',
            field=models.IntegerField(),
        ),
    ]