from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render
from players.models import Player, PlayerStatistics
from typing import Dict, Any

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

class MidfielderListView(PlayerListView):

    model = Player
    paginate_by = 50
    context_object_name = 'midfielder'






    

