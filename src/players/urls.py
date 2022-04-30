from django.urls import path
from django.views.generic import TemplateView
from players.views import PlayerDetailView, PlayerListView, MidfielderListView

urlpatterns = [
    path("", TemplateView.as_view(template_name='players/index.html'), name="home"),
    path("players/", PlayerListView.as_view(), name="player-list"),
    path("midfielders/", MidfielderListView.as_view(), name="midfielder-list"),
    path("players/<int:pk>/", PlayerDetailView.as_view(), name='player-detail')
]
