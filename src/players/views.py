from typing import Any, Dict

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from players.constants import DEFAULT_COLUMNS
from players.models import Player, PlayerStatistics

from .forms import EditProfileForm, PasswordChangingForm, SignUpForm


class PlayerListView(ListView):

    model = Player
    paginate_by = 50
    context_object_name = "players"


class Player2016ListView(ListView):

    model = PlayerStatistics.objects.filter(year=2016)
    paginate_by = 50
    context_object_name = "players"


class Player2017ListView(ListView):

    model = Player
    paginate_by = 50
    context_object_name = "players"


class Player2018ListView(ListView):

    model = Player
    paginate_by = 50
    context_object_name = "players"


class Player2019ListView(ListView):

    model = Player
    paginate_by = 50
    context_object_name = "players"


class Player2020ListView(ListView):

    model = Player
    paginate_by = 50
    context_object_name = "players"


class HomeView(ListView):

    model = Player
    context_object_name = "player"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["players_count"] = Player.objects.all().count()
        context["2016_count"] = PlayerStatistics.objects.filter(year="2016").count()
        context["2017_count"] = PlayerStatistics.objects.filter(year="2017").count()
        context["2018_count"] = PlayerStatistics.objects.filter(year="2018").count()
        context["2019_count"] = PlayerStatistics.objects.filter(year="2019").count()
        context["2020_count"] = PlayerStatistics.objects.filter(year="2020").count()

        return context


class PlayerDetailView(DetailView):

    model = Player
    context_object_name = "player"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["position_per_year"] = PlayerStatistics.objects.filter(
            player=self.get_object()
        ).values_list("year", "team_position")
        context["club_per_year"] = PlayerStatistics.objects.filter(
            player=self.get_object()
        ).values_list("year", "club")
        context["team_position"] = PlayerStatistics.objects.filter(
            player=self.get_object()
        ).values_list("team_position")
        context["statistics_list"] = [i.replace("_", " ") for i in DEFAULT_COLUMNS][7:]

        return context


class MidfielderListView(ListView):

    model = Player
    paginate_by = 50
    context_object_name = "midfielders"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["team_position"] = PlayerStatistics.objects.filter(team_position="LS")

        return context


class ProfileTemplateView(TemplateView):
    template_name = "registration/profile.html"


class PasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy("password-success")


class UserRegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")


class UserEditView(generic.UpdateView):
    form_class = EditProfileForm
    template_name = "registration/edit_profile.html"
    success_url = reverse_lazy("home")

    def get_object(self):
        return self.request.user


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy("password_success")


def password_success(request):
    return render(request, "registration/password_success.html", {})

def search_player(request):

    if request.method == "GET":
        searched = request.GET.get('searched')
        players = Player.objects.filter(short_name__icontains=searched)
        context = {'players': players}
        return render(request, 'players/player_search.html', context)
    else:
        return render(request, 'players/player_search.html', {})

