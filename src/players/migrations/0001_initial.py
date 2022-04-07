# Generated by Django 4.0.1 on 2022-04-02 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(max_length=100)),
                ('long_name', models.CharField(max_length=255)),
                ('nationality', models.CharField(max_length=100)),
                ('club', models.CharField(max_length=100)),
                ('age', models.CharField(max_length=100)),
                ('attacking_crossing', models.IntegerField(max_length=3)),
                ('attacking_finishing', models.IntegerField(max_length=3)),
                ('attacking_heading_accuracy', models.IntegerField(max_length=3)),
                ('attacking_short_passing', models.IntegerField(max_length=3)),
                ('attacking_volleys', models.IntegerField(max_length=3)),
                ('defending', models.IntegerField(max_length=3)),
                ('defending_marking', models.IntegerField(max_length=3)),
                ('defending_sliding_tackle', models.IntegerField(max_length=3)),
                ('defending_standing_tackle', models.IntegerField(max_length=3)),
                ('dribbling', models.IntegerField(max_length=3)),
                ('mentality_aggression', models.IntegerField(max_length=3)),
                ('mentality_interceptions', models.IntegerField(max_length=3)),
                ('mentality_penalties', models.IntegerField(max_length=3)),
                ('mentality_positioning', models.IntegerField(max_length=3)),
                ('mentality_vision', models.IntegerField(max_length=3)),
                ('movement_acceleration', models.IntegerField(max_length=3)),
                ('movement_agility', models.IntegerField(max_length=3)),
                ('movement_balance', models.IntegerField(max_length=3)),
                ('movement_reactions', models.IntegerField(max_length=3)),
                ('movement_sprint_speed', models.IntegerField(max_length=3)),
                ('pace', models.IntegerField(max_length=3)),
                ('passing', models.IntegerField(max_length=3)),
                ('physic', models.IntegerField(max_length=3)),
                ('power_jumping', models.IntegerField(max_length=3)),
                ('power_long_shots', models.IntegerField(max_length=3)),
                ('power_shot_power', models.IntegerField(max_length=3)),
                ('power_stamina', models.IntegerField(max_length=3)),
                ('power_strength', models.IntegerField(max_length=3)),
                ('shooting', models.IntegerField(max_length=3)),
                ('skill_ball_control', models.IntegerField(max_length=3)),
                ('skill_curve', models.IntegerField(max_length=3)),
                ('skill_dribbling', models.IntegerField(max_length=3)),
                ('skill_fk_accuracy', models.IntegerField(max_length=3)),
                ('skill_long_passing', models.IntegerField(max_length=3)),
                ('team_position', models.IntegerField(max_length=3)),
                ('player_positions', models.IntegerField(max_length=3)),
                ('overall', models.IntegerField(max_length=3)),
                ('value_eur', models.IntegerField(max_length=100)),
            ],
        ),
    ]