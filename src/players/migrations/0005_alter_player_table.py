# Generated by Django 4.0.1 on 2022-04-03 08:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0004_remove_player_player_positions_alter_player_age_and_more'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='player',
            table='players_table',
        ),
    ]