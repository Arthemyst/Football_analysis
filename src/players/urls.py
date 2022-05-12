from django.urls import path
from django.views.generic import TemplateView
from players.views import (HomeView, PasswordsChangeView, Player2016ListView,
                           Player2017ListView, Player2018ListView,
                           Player2019ListView, Player2020ListView,
                           PlayerDetailView, PlayerListView,
                           ProfileTemplateView, UserEditView, UserRegisterView)

urlpatterns = [
    path("", HomeView.as_view(template_name="players/index.html"), name="home"),
    path("players/2016/", Player2016ListView.as_view(), name="player-list-2016"),
    path("players/2017/", Player2017ListView.as_view(), name="player-list-2017"),
    path("players/2018/", Player2018ListView.as_view(), name="player-list-2018"),
    path("players/2019/", Player2019ListView.as_view(), name="player-list-2019"),
    path("players/2020/", Player2020ListView.as_view(), name="player-list-2020"),
    path("players/", PlayerListView.as_view(), name="player-list"),
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
]
