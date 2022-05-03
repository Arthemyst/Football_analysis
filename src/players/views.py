from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render
from players.models import Player, PlayerStatistics
from typing import Dict, Any
from django.shortcuts import  render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, View


class DefenderListView(ListView):
    model = Player
    paginate_by = 50
    context_object_name = 'player'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['defender'] = PlayerStatistics.objects.filter(team_position='LAM')

        return context

class PlayerListView(ListView):

    model = Player
    paginate_by = 50
    context_object_name = 'players'

class PlayerDetailView(DetailView):

    model = Player
    context_object_name = 'player'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['pace_per_year'] = PlayerStatistics.objects.filter(player=self.get_object()).values_list("year", "overall")

        return context

class MidfielderListView(ListView):
    model = Player
    paginate_by = 50
    context_object_name = 'player'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['midfielder'] = PlayerStatistics.objects.filter(team_position='LAM')

        return context
