import pytest
from players.models import Player, PlayerStatistics


@pytest.fixture
def player_messi(db):
    player = Player.objects.create(
        short_name="L. Messi",
        long_name="Lionel Andrés Messi Cuccittini",
        nationality="Argentina")

    PlayerStatistics.objects.create(
        player=player,
        year=2019,
        team_position="ATK",
        club="FC Barcelona",
        age=30,
        overall=90,
        value_eur=90000000,
        pace=90,
        shooting=90,
        passing=90,
        dribbling=90,
        defending=50,
        physic=60,
        attacking_crossing=90,
        attacking_finishing=90,
        attacking_heading_accuracy=90,
        attacking_short_passing=90,
        attacking_volleys=80,
        skill_dribbling=92,
        skill_curve=90,
        skill_fk_accuracy=90,
        skill_long_passing=90,
        skill_ball_control=90,
        movement_acceleration=90,
        movement_sprint_speed=90,
        movement_agility=90,
        movement_reactions=90,
        movement_balance=90,
        power_shot_power=90,
        power_jumping=90,
        power_stamina=90,
        power_strength=90,
        power_long_shots=90,
        mentality_aggression=90,
        mentality_interceptions=90,
        mentality_positioning=90,
        mentality_vision=90,
        mentality_penalties=90,
        defending_marking=90,
        defending_standing_tackle=90,
        defending_sliding_tackle=90,
    )
    return player