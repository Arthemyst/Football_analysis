from django.db import models


class Player(models.Model):

    short_name = models.CharField(max_length=50)
    long_name = models.CharField(max_length=100)
    nationality = models.CharField(max_length=50)

    def __str__(self):
        return self.short_name



class PlayerStatistics(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    year = models.PositiveSmallIntegerField()
    team_position = models.CharField(max_length=50)
    club = models.CharField(max_length=50)
    age = models.PositiveSmallIntegerField()
    overall = models.PositiveSmallIntegerField()
    value_eur = models.PositiveIntegerField()
    pace = models.PositiveSmallIntegerField()
    shooting = models.PositiveSmallIntegerField()
    passing = models.PositiveSmallIntegerField()
    dribbling = models.PositiveSmallIntegerField()
    defending = models.PositiveSmallIntegerField()
    physic = models.PositiveSmallIntegerField()
    attacking_crossing = models.PositiveSmallIntegerField()
    attacking_finishing = models.PositiveSmallIntegerField()
    attacking_heading_accuracy = models.PositiveSmallIntegerField()
    attacking_short_passing = models.PositiveSmallIntegerField()
    attacking_volleys = models.PositiveSmallIntegerField()
    skill_dribbling = models.PositiveSmallIntegerField()
    skill_curve = models.PositiveSmallIntegerField()
    skill_fk_accuracy = models.PositiveSmallIntegerField()
    skill_long_passing = models.PositiveSmallIntegerField()
    skill_ball_control = models.PositiveSmallIntegerField()
    movement_acceleration = models.PositiveSmallIntegerField()
    movement_sprint_speed = models.PositiveSmallIntegerField()
    movement_agility = models.PositiveSmallIntegerField()
    movement_reactions = models.PositiveSmallIntegerField()
    movement_balance = models.PositiveSmallIntegerField()
    power_shot_power = models.PositiveSmallIntegerField()
    power_jumping = models.PositiveSmallIntegerField()
    power_stamina = models.PositiveSmallIntegerField()
    power_strength = models.PositiveSmallIntegerField()
    power_long_shots = models.PositiveSmallIntegerField()
    mentality_aggression = models.PositiveSmallIntegerField()
    mentality_interceptions = models.PositiveSmallIntegerField()
    mentality_positioning = models.PositiveSmallIntegerField()
    mentality_vision = models.PositiveSmallIntegerField()
    mentality_penalties = models.PositiveSmallIntegerField()
    defending_marking = models.PositiveSmallIntegerField()
    defending_standing_tackle = models.PositiveSmallIntegerField()
    defending_sliding_tackle = models.PositiveSmallIntegerField()

    class Meta:
        unique_together=[['player', 'year']] 
