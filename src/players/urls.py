from django.urls import path
from django.views.generic import TemplateView
from players.views import PlayerDetailView, PlayerListView, MidfielderListView, DefenderListView, SignUpView
from . import views

urlpatterns = [
    path("", TemplateView.as_view(template_name='players/index.html'), name="home"),
    path("midfielders/", MidfielderListView.as_view(), name="midfielder-list"),
    path("players/", PlayerListView.as_view(), name="player-list"),
    path("defenders/", DefenderListView.as_view(), name="defender-list"),
    path("players/<int:pk>/", PlayerDetailView.as_view(), name='player-detail'),
    path('signup/', SignUpView.as_view(), name='signup'),
]
