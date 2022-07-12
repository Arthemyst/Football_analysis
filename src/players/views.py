

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
from django.core.paginator import Paginator
import plotly.express as px
import plotly.graph_objects as go


from .forms import EditProfileForm, PasswordChangingForm, SignUpForm


class PlayerListView(ListView):

    model = Player
    paginate_by = 50
    context_object_name = "players"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["players_all"] = Player.objects.all()
        return context


class HomeView(ListView):

    model = Player
    context_object_name = "player"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["players_count"] = Player.objects.all().count()

        return context


class PlayerDetailView(DetailView):

    model = Player
    context_object_name = "player"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["position_per_year"] = PlayerStatistics.objects.filter(
            player=self.get_object()
        ).values_list("year", "team_position")
        context["value_per_year"] = PlayerStatistics.objects.filter(
            player=self.get_object()
        ).values_list("year", "value_eur")

        context["club_per_year"] = PlayerStatistics.objects.filter(
            player=self.get_object()
        ).values_list("year", "club")
        context["team_position"] = PlayerStatistics.objects.filter(
            player=self.get_object()
        ).values_list("team_position")
        context["statistics_list"] = [i.replace("_", " ") for i in DEFAULT_COLUMNS][7:]
        overall_year = PlayerStatistics.objects.filter(
            player=self.get_object()
        ).values_list("overall", "year").order_by('year')
        fig = px.line(
            x = [c[1] for c in overall_year],
            y = [c[0] for c in overall_year],
            markers=True,
            labels = {'x': 'Year', 'y': 'Overall'},
            height=325
        )
        fig.update_xaxes(dtick='d')
        fig.update_yaxes(dtick='d')
        chart = fig.to_html()
        context["chart"] = chart
        return context


class ProfileTemplateView(TemplateView):
    template_name = "registration/profile.html"


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
        searched = request.GET.get("searched")
        players = Player.objects.filter(short_name__icontains=searched).order_by("id")
        paginator = Paginator(players, 25)

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {"players": players, "page_obj": page_obj, "searched": searched}

        return render(request, "players/player_search.html", context)
    else:
        return render(request, "players/player_search.html", {})


class ClubFinderView(TemplateView):
    model = Player
    template_name = "players/club_search.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["clubs"] = (
            PlayerStatistics.objects.order_by("club").values("club").distinct()
        )

        return context


def search_club(request):

    if request.method == "GET":
        searched = request.GET.get("searched_club")
        players = Player.objects.filter(
            playerstatistics__club__icontains=searched, playerstatistics__year=2020
        ).order_by("id")
        context = {"players": players, "searched": searched}
        return render(request, "players/players_in_club.html", context)
    else:
        return render(request, "players/players_in_club.html", {})


class PlayersCompareView(ListView):
    model = Player
    template_name = "players/compare_players.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["players"] = (
            Player.objects.order_by("id").values("long_name").distinct()
        )

        return context


def compare_players(request):

    if request.method == "GET":
        searched_player1 = request.GET.get("player1")
        searched_player2 = request.GET.get("player2")

        player1 = Player.objects.filter(
            playerstatistics__player__long_name__icontains=searched_player1,
            playerstatistics__year=2020,
        )
        player2 = Player.objects.filter(
            playerstatistics__player__long_name__icontains=searched_player2,
            playerstatistics__year=2020,
        )
        player1_position = PlayerStatistics.objects.filter(
            player__long_name__icontains=searched_player1
        ).values_list("team_position")
        player2_position = PlayerStatistics.objects.filter(
            player__long_name=searched_player2
        ).values_list("team_position")
        player1_position_per_year = PlayerStatistics.objects.filter(
            player__long_name=searched_player1
        ).values_list("year", "team_position")
        player2_position_per_year = PlayerStatistics.objects.filter(
            player__long_name=searched_player2
        ).values_list("year", "team_position")
        player1_value_per_year = PlayerStatistics.objects.filter(
            player__long_name=searched_player1
        ).values_list("year", "value_eur")
        player2_value_per_year = PlayerStatistics.objects.filter(
            player__long_name=searched_player2
        ).values_list("year", "value_eur")
        player1_club_per_year = PlayerStatistics.objects.filter(
            player__long_name=searched_player1
        ).values_list("year", "club")
        player2_club_per_year = PlayerStatistics.objects.filter(
            player__long_name=searched_player2
        ).values_list("year", "club")
        player1_long_name = Player.objects.filter(
            long_name=searched_player1
        ).values_list("long_name")
        player2_long_name = Player.objects.filter(
            long_name=searched_player2
        ).values_list("long_name")
        player1_nationality = Player.objects.filter(
            long_name=searched_player1
        ).values_list("nationality")
        player2_nationality = Player.objects.filter(
            long_name=searched_player2
        ).values_list("nationality")
        player1_overall_per_year = PlayerStatistics.objects.filter(
            player__long_name=searched_player1
        ).values_list("year", "overall")
        player2_overall_per_year = PlayerStatistics.objects.filter(
            player__long_name=searched_player2
        ).values_list("year", "overall")
        player1_value_per_year = PlayerStatistics.objects.filter(
            player__long_name=searched_player1
        ).values_list("value_eur", "year").order_by('year')
        player2_value_per_year = PlayerStatistics.objects.filter(
            player__long_name=searched_player2
        ).values_list("value_eur", "year").order_by('year')
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x = [c[1] for c in player1_value_per_year],
            y = [c[0] for c in player1_value_per_year],
            name=f'{searched_player1}'

        ))
        fig.add_trace(go.Scatter(
            x = [c[1] for c in player2_value_per_year],
            y = [c[0] for c in player2_value_per_year],
            name=f'{searched_player2}'
            
        ))
        fig.update_layout(xaxis_title="Year", yaxis_title="Value in Euro")
        fig.update_xaxes(dtick='d')
        #fig.update_yaxes(dtick='d')
        chart = fig.to_html()
        
        context = {
            "player1": player1,
            "player2": player2,
            "player1_position": player1_position,
            "player2_position": player2_position,
            "player1_position_per_year": player1_position_per_year,
            "player2_position_per_year": player2_position_per_year,
            "player1_value_per_year": player1_value_per_year,
            "player2_value_per_year": player2_value_per_year,
            "player1_club_per_year": player1_club_per_year,
            "player2_club_per_year": player2_club_per_year,
            "player1_long_name": player1_long_name,
            "player2_long_name": player2_long_name,
            "player1_nationality": player1_nationality,
            "player2_nationality": player2_nationality,
            "player1_overall_per_year": player1_overall_per_year,
            "player2_overall_per_year": player2_overall_per_year,
            "chart": chart,
        }
        return render(request, "players/compare_chosen_players.html", context)
    else:
        return render(request, "players/compare_chosen_players.html.html", {})


class PlayerSearchView(ListView):
    model = Player
    template_name = "players/player_search.html"

    paginate_by: 50

    def get_queryset(self):
        searched = self.kwargs.get("searched")

        if searched:
            players = Player.objects.filter(short_name__icontains=searched)
            if len(players) == 0:
                players = None
            else:
                players = players
        else:
            players = None
        return players
