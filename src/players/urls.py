from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from players.views import (
    ClubFinderView,
    HomeView,
    PasswordsChangeView,
    PlayerDetailView,
    PlayerListView,
    PlayersCompareView,
    ProfileTemplateView,
    UserEditView,
    UserRegisterView,
    attacker_value_estimation,
    compare_players,
    defender_value_estimation,
    midfielder_value_estimation,
    search_club,
    search_club_year,
    search_player,
    PlayerDetailByNameAPI,
    ClubPlayersAPI,
    DashboardStatsAPI, PlayersListAPI,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Football API",
        default_version="v1",
        description="API for gathering information about Football players from Fifa game (years 2016-2019)",
    ),
    public=False,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("", HomeView.as_view(template_name="players/index.html"), name="home"),
    path("players/all/", PlayerListView.as_view(), name="player-list"),
    path("players/<int:pk>/", PlayerDetailView.as_view(), name="player-detail"),
    path("profile/", ProfileTemplateView.as_view(), name="profile"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("edit_profile/", UserEditView.as_view(), name="edit-profile"),
    path(
        "password/",
        PasswordsChangeView.as_view(template_name="registration/change-password.html"),
        name="password",
    ),
    path(
        "password_success/",
        PasswordsChangeView.as_view(template_name="registration/password_success.html"),
        name="password-success",
    ),
    path("player_search/", search_player, name="player-search"),
    path("club_search/", ClubFinderView.as_view(), name="club-search"),
    path("club_searched/", search_club, name="players-in-club"),
    path("compare_searched_players/", compare_players, name="compare-searched-players"),
    path("compare_players/", PlayersCompareView.as_view(), name="compare-players"),
    path("club_searched/year/", search_club_year, name="players-in-club-year"),
    path(
        "midfielder_value_estimation/",
        midfielder_value_estimation,
        name="midfielder-value-estimation",
    ),
    path(
        "attacker_value_estimation/",
        attacker_value_estimation,
        name="attacker-value-estimation",
    ),
    path(
        "defender_value_estimation/",
        defender_value_estimation,
        name="defender-value-estimation",
    ),
    path("api/players/", PlayersListAPI.as_view(), name="players-list-api"),
    path("api/player/<str:short_name>/", PlayerDetailByNameAPI.as_view(), name="player-detail-api"),
    path("api/club-players/", ClubPlayersAPI.as_view(), name="club-players-api"),
    path("api/dashboard/", DashboardStatsAPI.as_view(), name="dashboard-stats-api"),
    path("swagger-api/", schema_view.with_ui('swagger', cache_timeout=0), name="schema-swagger-ui"),
    re_path(r'^swagger-api(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('redoc-api/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
