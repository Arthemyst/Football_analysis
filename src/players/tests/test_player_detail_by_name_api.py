import pytest
from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from players.tests.fixtures.player_fixture import player_messi

from players.models import UserActivity


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


    def test_auth_required(self, api_client, player_messi):
        url = reverse("player-detail-api", kwargs={"short_name": player_messi.short_name})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_player_detail_success(self, api_client, user, player_messi):
        api_client.force_authenticate(user=user)
        url = reverse("player-detail-api", kwargs={"short_name": player_messi.short_name})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["short_name"] == player_messi.short_name
        assert response.data["long_name"] == player_messi.long_name

        activity = UserActivity.objects.filter(
            user=user, action="viewed_player_by_api"
        ).first()
        assert activity is not None
        assert activity.detail["short_name"] == player_messi.short_name

    def test_player_not_found(self, api_client, user):
        api_client.force_authenticate(user=user)
        url = reverse("player-detail-api", kwargs={"short_name": "Unknown"})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "error" in response.data
