import pytest
from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from players.models import Player, PlayerStatistics, UserActivity


@pytest.mark.django_db
class TestPlayersByNameAPI:
    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def user(self, django_user_model):
        return django_user_model.objects.create_user(
            username="testuser",
            password="testpassword",
            email="email@email.com"
        )

    @pytest.fixture(autouse=True)
    def clear_cache_fixture(self):
        cache.clear()

    @pytest.fixture
    def get_player(self):
        player = Player.objects.create(
            short_name="L. Messi",
            long_name="Lionel Andrés Messi Cuccittini",
            nationality="Argentina"
        )
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

    def test_auth_required(self, api_client, get_player):
        url = reverse("player-detail-api", kwargs={"short_name": get_player.short_name})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_player_detail_success(self, api_client, user, get_player):
        api_client.force_authenticate(user=user)
        url = reverse("player-detail-api", kwargs={"short_name": get_player.short_name})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["short_name"] == get_player.short_name
        assert response.data["long_name"] == get_player.long_name

        activity = UserActivity.objects.filter(
            user=user, action="viewed_player_by_api"
        ).first()
        assert activity is not None
        assert activity.detail["short_name"] == get_player.short_name

    def test_player_not_found(self, api_client, user):
        api_client.force_authenticate(user=user)
        url = reverse("player-detail-api", kwargs={"short_name": "Unknown"})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "error" in response.data
