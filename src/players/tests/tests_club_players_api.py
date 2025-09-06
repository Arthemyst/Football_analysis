import pytest
from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from players.models import UserActivity
from players.throttling import ClubPlayersThrottle
from players.tests.fixtures.player_fixture import player_messi

@pytest.mark.django_db
class TestClubPlayersAPI:
    endpoint = reverse('club-players-api')

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

    def test_auth_required(self, api_client):
        response = api_client.get(self.endpoint)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_missing_club_param(self, api_client, user):
        api_client.force_authenticate(user=user)
        response = api_client.get(self.endpoint)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.data

    def test_get_players_by_club(self, api_client, user, player_messi):

        api_client.force_authenticate(user=user)
        response = api_client.get(self.endpoint, {'club': "FC Barcelona"})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["club"] == "FC Barcelona"
        assert len(response.data["players"]) == 1
        assert response.data["players"][0]["short_name"] == "L. Messi"

        activity = UserActivity.objects.last()
        assert activity.action == "searched_club_by_api"
        assert activity.detail["club"] == "FC Barcelona"

    def test_cache_hit(self, api_client, user, monkeypatch):
        api_client.force_authenticate(user=user)

        club = "Real Madrid"
        year = 2020
        cache_key = f"club_players:{club}:{year}"

        cached_data = {"club": club, "year": year, "players": [{"short_name": "Fake"}]}
        cache.set(cache_key, cached_data, timeout=3600)

        monkeypatch.setattr(ClubPlayersThrottle, "allow_request", lambda *a, **kw: True)

        response = api_client.get(self.endpoint, {"club": club, "year": year})
        assert response.status_code == status.HTTP_200_OK
        assert response.data == cached_data
