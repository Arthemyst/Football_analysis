import pytest
from django.core.exceptions import ValidationError
from django.db.utils import DataError, IntegrityError

from players.models import Player, PlayerStatistics


@pytest.fixture
def valid_player_data():
    return dict(
        short_name="L. Messi",
        long_name="Lionel Andrés Messi Cuccittini",
        nationality="Argentina"
    )


@pytest.fixture
def player():
    return Player.objects.create(
        short_name="L. Messi",
        long_name="Lionel Andrés Messi Cuccittini",
        nationality="Argentina"
    )


@pytest.fixture
def valid_statistics_data(player):
    return dict(
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


@pytest.mark.django_db
class TestPlayerModel:
    def test_create_valid_player(self, valid_player_data):
        player = Player.objects.create(**valid_player_data)

        assert player.id is not None
        assert player.short_name == "L. Messi"
        assert player.long_name == "Lionel Andrés Messi Cuccittini"
        assert player.nationality == "Argentina"

    def test_missing_required_field(self, valid_player_data):
        valid_player_data.pop("short_name")

        player = Player(**valid_player_data)
        with pytest.raises(ValidationError):
            player.full_clean()


@pytest.mark.django_db
class TestPlayerStatisticsModel:

    def test_create_valid_player_statistics(self, valid_statistics_data):
        statistics = PlayerStatistics.objects.create(**valid_statistics_data)

        assert statistics.id is not None
        assert statistics.player.short_name == "L. Messi"
        assert statistics.year == 2019
        assert statistics.team_position == "ATK"
        assert statistics.club == "FC Barcelona"
        assert statistics.age == 30
        assert statistics.overall == 90
        assert statistics.value_eur == 90000000
        assert statistics.pace == 90

    def test_invalid_age_type_validation(self, valid_statistics_data):
        valid_statistics_data["age"] = "two"
        stats = PlayerStatistics(**valid_statistics_data)

        with pytest.raises(ValidationError):
            stats.full_clean()

    def test_unique_constraint_example(self, valid_statistics_data):
        PlayerStatistics.objects.create(**valid_statistics_data)

        with pytest.raises(IntegrityError):
            PlayerStatistics.objects.create(**valid_statistics_data)

    def test_invalid_club_name_too_long(self, valid_statistics_data):
        valid_statistics_data["club"] = "X" * 300
        stats = PlayerStatistics(**valid_statistics_data)

        with pytest.raises(DataError):
            stats.save()
