import pytest
from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from players.models import Player, UserActivity


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username="testuser",
        password="testpassword",
        email="email@email.com"
    )


@pytest.mark.django_db
class TestPlayersListAPI:

    @pytest.fixture(autouse=True)
    def clear_cache_fixture(self):
        cache.clear()

    @pytest.fixture
    def players(self):
        players = [
            Player.objects.create(short_name=f"Player{i}", long_name=f"Player {i} Long Name", nationality="Country")
            for i in range(1, 6)
        ]
        return players

    def test_auth_required(self, api_client):
        url = reverse("players-list-api")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_players_authenticated(self, api_client, user, players):
        api_client.force_authenticate(user=user)
        url = reverse("players-list-api")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == len(players)

        for item in response.data["results"]:
            assert "short_name" in item
            assert "long_name" in item

    def test_user_activity_logged(self, api_client, user, players):
        api_client.force_authenticate(user=user)
        url = reverse("players-list-api")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

        activity = UserActivity.objects.filter(
            user=user, action="viewed_players_list_by_api"
        ).first()
        assert activity is not None
        assert activity.detail["page"] == 1
        assert activity.detail["page_size"] == 20

    def test_cache_is_used(self, api_client, user, players):
        api_client.force_authenticate(user=user)
        url = reverse("players-list-api")

        response1 = api_client.get(url)
        assert response1.status_code == status.HTTP_200_OK

        Player.objects.create(short_name="NewPlayer", long_name="New Player Full", nationality="Country")
        response2 = api_client.get(url)
        assert len(response2.data["results"]) == len(players)

    def test_invalid_page_number(self, api_client, user, players):
        api_client.force_authenticate(user=user)
        url = reverse("players-list-api") + "?page=invalid"
        response = api_client.get(url)
        # DRF is setting default page = 1
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == len(players)

    def test_invalid_page_size(self, api_client, user, players):
        api_client.force_authenticate(user=user)
        url = reverse("players-list-api") + "?page_size=invalid"
        response = api_client.get(url)
        # DRF is setting default page size = 20
        assert response.status_code == status.HTTP_200_OK
