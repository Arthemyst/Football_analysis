import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestDashboardStatsAPI:
    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def admin_user(self, django_user_model):
        return django_user_model.objects.create_superuser(
            username="admin",
            password="adminpass",
            email="admin@example.com"
        )

    @pytest.fixture
    def normal_user(self, django_user_model):
        return django_user_model.objects.create_user(
            username="user",
            password="userpass",
            email="user@example.com"
        )

    def test_auth_required(self, api_client):
        url = reverse("dashboard-stats-api")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_only_admin_has_access(self, api_client, normal_user):
        api_client.force_authenticate(user=normal_user)
        url = reverse("dashboard-stats-api")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_access_success(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)
        url = reverse("dashboard-stats-api")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert "players_comparison" in response.data or "players_list_usage" in response.data
