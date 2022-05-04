from django.urls import path
from django.views.generic import TemplateView
from players.views import PlayerDetailView, PlayerListView, MidfielderListView, ProfileTemplateView, HomeView

urlpatterns = [
    path("", HomeView.as_view(template_name='players/index.html'), name="home"),
    path("midfielders/", MidfielderListView.as_view(), name="midfielder-list"),
    path("players/", PlayerListView.as_view(), name="player-list"),
    path("players/<int:pk>/", PlayerDetailView.as_view(), name='player-detail'),
    path('profile/', ProfileTemplateView.as_view(), name='profile')
]