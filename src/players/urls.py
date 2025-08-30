from django.urls import path

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
    PlayerDetailByNameAPI, ClubPlayersAPI,
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
    path("api/player/<str:short_name>/", PlayerDetailByNameAPI.as_view(), name="player-detail-api"),
    path("api/club-players/", ClubPlayersAPI.as_view(), name="club-players-api"),
]
