import os
from math import floor, log
from typing import Any, Dict

import joblib
import plotly.graph_objects as go
from django.contrib.auth.views import PasswordChangeView
from django.core.paginator import Paginator
from django.core.cache import cache
from django.db.models import Count
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from players.constants import DEFAULT_COLUMNS
from players.models import Player, PlayerStatistics, UserActivity
from players.serializers import PlayersSerializer, PlayerBasicSerializer, PlayerListSerializer
from .forms import EditProfileForm, PasswordChangingForm, SignUpForm

mid_model_path = "players/models/model_midfield.pkl"
att_model_path = "players/models/model_attack.pkl"
def_model_path = "players/models/model_defend.pkl"

if os.path.exists(mid_model_path):
    model_mid = joblib.load(mid_model_path)
else:
    model_mid = None
if os.path.exists(att_model_path):
    model_att = joblib.load(att_model_path)
else:
    model_att = None
if os.path.exists(def_model_path):
    model_def = joblib.load(def_model_path)
else:
    model_def = None


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        player = self.get_object()

        if self.request.user.is_authenticated:
            from .models import UserActivity
            UserActivity.objects.create(
                user=self.request.user,
                action="viewed_player_by_website",
                detail={"short_name": player.short_name, "long_name": player.long_name}
            )

        chosen_statistic = self.request.GET.get("chosen_statistic", "overall").replace(" ", "_")

        player_statistics = PlayerStatistics.objects.filter(player=player)
        chosen_statistic_year = player_statistics.values_list(chosen_statistic, "year").order_by("year")

        context["position_per_year"] = player_statistics.values_list("year", "team_position")
        context["value_per_year"] = player_statistics.values_list("year", "value_eur")
        context["club_per_year"] = player_statistics.values_list("year", "club")
        context["team_position"] = player_statistics.values_list("team_position")
        context["statistics_list"] = [i.replace("_", " ") for i in DEFAULT_COLUMNS][7:]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[c[1] for c in chosen_statistic_year], y=[c[0] for c in chosen_statistic_year]))
        fig.update_xaxes(dtick="d")
        fig.update_layout(xaxis_title="Year", yaxis_title=chosen_statistic.replace("_", " "))
        if chosen_statistic != "value_eur":
            fig.update_yaxes(dtick="d")
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
        request.session["save_searched_club"] = searched
        request.session.modified = True
        years = PlayerStatistics.objects.filter(club=searched).order_by()
        if not years:
            return render(request, "players/players_in_club.html", {})
        else:
            years_distinct = list(set([year.year for year in years]))
            last_year = years_distinct[-1]
            players = Player.objects.filter(
                playerstatistics__club__icontains=searched,
                playerstatistics__year=last_year,
            ).order_by("id")
            club_name = list(set([player.club for player in years]))[0]
            context = {
                "players": players,
                "searched": searched,
                "years": years_distinct,
                "club_name": club_name,
                "last_year": last_year,
            }
            return render(request, "players/players_in_club.html", context)
    else:
        return render(request, "players/players_in_club.html", {})


def search_club_year(request):
    if request.method == "GET":
        searched = request.session["save_searched_club"]
        request.session["save_searched_club"] = searched
        request.session.modified = True
        years = PlayerStatistics.objects.filter(club=searched).order_by()
        years_distinct = list(set([year.year for year in years]))
        if not years_distinct:
            last_year = 2020
        else:
            last_year = max(years_distinct)

        year = request.GET.get("year", last_year)

        players = Player.objects.filter(
            playerstatistics__club__icontains=searched, playerstatistics__year=year
        ).order_by("id")
        club_name = PlayerStatistics.objects.filter(club=searched).first().club
        context = {
            "players": players,
            "searched": searched,
            "years": years_distinct,
            "club_name": club_name,
            "year": year,
        }
        return render(request, "players/players_in_club_year.html", context)
    else:
        return render(request, "players/players_in_club_year.html", {})


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

        if searched_player1 == searched_player2:
            same_players = True
            context = {"same_players": same_players}
        else:
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
            player1_position_per_year = (
                PlayerStatistics.objects.filter(player__long_name=searched_player1)
                .values_list("year", "team_position")
                .order_by("year")
            )
            player2_position_per_year = (
                PlayerStatistics.objects.filter(player__long_name=searched_player2)
                .values_list("year", "team_position")
                .order_by("year")
            )
            player1_club_per_year = (
                PlayerStatistics.objects.filter(player__long_name=searched_player1)
                .values_list("year", "club")
                .order_by("year")
            )
            player2_club_per_year = (
                PlayerStatistics.objects.filter(player__long_name=searched_player2)
                .values_list("year", "club")
                .order_by("year")
            )
            player1_long_name = Player.objects.filter(
                long_name=searched_player1
            ).values_list("long_name")
            player2_long_name = Player.objects.filter(
                long_name=searched_player2
            ).values_list("long_name")
            player1_short_name = Player.objects.filter(
                long_name=searched_player1
            ).values_list("short_name")
            player2_short_name = Player.objects.filter(
                long_name=searched_player2
            ).values_list("short_name")
            player1_nationality = Player.objects.filter(
                long_name=searched_player1
            ).values_list("nationality")
            player2_nationality = Player.objects.filter(
                long_name=searched_player2
            ).values_list("nationality")
            player1_value_per_year = (
                PlayerStatistics.objects.filter(player__long_name=searched_player1)
                .values_list("value_eur", "year")
                .order_by("year")
            )
            player2_value_per_year = (
                PlayerStatistics.objects.filter(player__long_name=searched_player2)
                .values_list("value_eur", "year")
                .order_by("year")
            )

            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=[c[1] for c in player1_value_per_year],
                    y=[c[0] for c in player1_value_per_year],
                    name=f"{searched_player1}",
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=[c[1] for c in player2_value_per_year],
                    y=[c[0] for c in player2_value_per_year],
                    name=f"{searched_player2}",
                )
            )
            fig.update_xaxes(dtick="d")
            fig.update_layout(xaxis_title="Year", yaxis_title="Value eur")
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
                "player1_short_name": player1_short_name,
                "player2_short_name": player2_short_name,
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


def defender_value_estimation(request):
    if request.method == "POST":
        defending = request.POST.get("defending")
        defending_marking = request.POST.get("defending_marking")
        defending_sliding_tackle = request.POST.get("defending_sliding_tackle")
        defending_standing_tackle = request.POST.get("defending_standing_tackle")
        movement_reactions = request.POST.get("movement_reactions")
        mentality_interceptions = request.POST.get("mentality_interceptions")
        defending = request.POST.get("defending")

        if model_def != None:
            pred_value = change_number_format(
                int(
                    model_def.predict(
                        [
                            [
                                defending,
                                defending_marking,
                                defending_sliding_tackle,
                                defending_standing_tackle,
                                mentality_interceptions,
                                movement_reactions,
                            ]
                        ]
                    )[0]
                )
            )

            euro = "euro"
        else:
            pred_value = "Result will be soon..."
            euro = ""
        context = {
            "defending": defending,
            "defending_marking": defending_marking,
            "defending_sliding_tackle": defending_sliding_tackle,
            "defending_standing_tackle": defending_standing_tackle,
            "mentality_interceptions": mentality_interceptions,
            "movement_reactions": movement_reactions,
            "pred_value": pred_value,
            "euro": euro,
        }
        return render(request, "players/defender_value_estimation.html", context)
    else:
        context = {
            "defending": 75,
            "defending_marking": 75,
            "defending_sliding_tackle": 75,
            "defending_standing_tackle": 75,
            "mentality_interceptions": 75,
            "movement_reactions": 75,
            "pred_value": "Click estimation button",
            "euro": "",
        }
        return render(request, "players/defender_value_estimation.html", context)


def attacker_value_estimation(request):
    if request.method == "POST":
        attacking_finishing = request.POST.get("attacking_finishing")
        attacking_short_passing = request.POST.get("attacking_short_passing")
        dribbling = request.POST.get("dribbling")
        mentality_positioning = request.POST.get("mentality_positioning")
        movement_reactions = request.POST.get("movement_reactions")
        passing = request.POST.get("passing")
        shooting = request.POST.get("shooting")
        skill_ball_control = request.POST.get("skill_ball_control")
        skill_dribbling = request.POST.get("skill_dribbling")
        if model_att:
            pred_value = change_number_format(
                int(
                    model_att.predict(
                        [
                            [
                                attacking_finishing,
                                attacking_short_passing,
                                dribbling,
                                mentality_positioning,
                                movement_reactions,
                                passing,
                                shooting,
                                skill_ball_control,
                                skill_dribbling,
                            ]
                        ]
                    )[0]
                )
            )
            euro = "euro"
        else:
            pred_value = "Result will be soon..."
            euro = ""
        context = {
            "attacking_finishing": attacking_finishing,
            "attacking_short_passing": attacking_short_passing,
            "dribbling": dribbling,
            "mentality_positioning": mentality_positioning,
            "movement_reactions": movement_reactions,
            "passing": passing,
            "shooting": shooting,
            "skill_ball_control": skill_ball_control,
            "skill_dribbling": skill_dribbling,
            "euro": euro,
            "pred_value": pred_value,
        }
        return render(request, "players/attacker_value_estimation.html", context)
    else:
        context = {
            "attacking_finishing": 75,
            "attacking_short_passing": 75,
            "dribbling": 75,
            "mentality_positioning": 75,
            "movement_reactions": 75,
            "passing": 75,
            "shooting": 75,
            "skill_ball_control": 75,
            "skill_dribbling": 75,
            "pred_value": "Click estimation button",
            "euro": "",
        }
        return render(request, "players/attacker_value_estimation.html", context)


def midfielder_value_estimation(request):
    if request.method == "POST":
        attacking_short_passing = request.POST.get("attacking_short_passing")
        dribbling = request.POST.get("dribbling")
        mentality_positioning = request.POST.get("mentality_positioning")
        mentality_vision = request.POST.get("mentality_vision")
        movement_reactions = request.POST.get("movement_reactions")
        passing = request.POST.get("passing")
        shooting = request.POST.get("shooting")
        skill_ball_control = request.POST.get("skill_ball_control")
        skill_dribbling = request.POST.get("skill_dribbling")
        skill_long_passing = request.POST.get("skill_long_passing")

        if model_mid:
            pred_value = change_number_format(
                int(
                    model_mid.predict(
                        [
                            [
                                attacking_short_passing,
                                dribbling,
                                mentality_positioning,
                                mentality_vision,
                                movement_reactions,
                                passing,
                                shooting,
                                skill_ball_control,
                                skill_dribbling,
                                skill_long_passing,
                            ]
                        ]
                    )[0]
                )
            )
            euro = "euro"
        else:
            pred_value = "Result will be soon..."
            euro = ""

        context = {
            "attacking_short_passing": attacking_short_passing,
            "dribbling": dribbling,
            "mentality_positioning": mentality_positioning,
            "mentality_vision": mentality_vision,
            "movement_reactions": movement_reactions,
            "passing": passing,
            "shooting": shooting,
            "skill_ball_control": skill_ball_control,
            "skill_dribbling": skill_dribbling,
            "skill_long_passing": skill_long_passing,
            "euro": euro,
            "pred_value": pred_value,
        }
        return render(request, "players/midfielder_value_estimation.html", context)
    else:
        context = {
            "attacking_short_passing": 75,
            "dribbling": 75,
            "mentality_positioning": 75,
            "mentality_vision": 75,
            "movement_reactions": 75,
            "passing": 75,
            "shooting": 75,
            "skill_ball_control": 75,
            "skill_dribbling": 75,
            "skill_long_passing": 75,
            "pred_value": "Click estimation button",
            "euro": "",
        }
        return render(request, "players/midfielder_value_estimation.html", context)


class PlayerDetailByNameAPI(RetrieveAPIView):
    serializer_class = PlayersSerializer
    lookup_field = "short_name"
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Player.objects.all()

    @swagger_auto_schema(
        operation_description="Returns detailed information about a player by their short_name.",
        manual_parameters=[
            openapi.Parameter(
                name="short_name",
                in_=openapi.IN_PATH,
                description="The short name of the player (e.g., 'L. Messi').",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: PlayersSerializer,
        },
    )
    def get(self, request, *args, **kwargs):
        short_name = kwargs.get("short_name")

        cache_key = f"player_detail:{short_name.lower()}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        try:
            player = Player.objects.get(short_name__iexact=short_name)
            UserActivity.objects.create(
                user=request.user,
                action="viewed_player_by_api",
                detail={"short_name": kwargs.get("short_name")},
            )
        except Player.DoesNotExist:
            return Response({"error": f"Player '{short_name}' not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(player)
        response_data = serializer.data


        cache.set(cache_key, response_data, timeout=60 * 60 * 24)

        return Response(response_data)

class ClubPlayersAPI(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description=(
                "Returns a list of players who played for a given club. "
                "Optionally filter by year."
        ),
        manual_parameters=[
            openapi.Parameter(
                name="club",
                in_=openapi.IN_QUERY,
                description="Club name (required). Example: `Real Madrid`",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                name="year",
                in_=openapi.IN_QUERY,
                description="Season year (optional). Example: `2020`",
                type=openapi.TYPE_INTEGER,
                required=False,
            ),
        ],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "club": openapi.Schema(type=openapi.TYPE_STRING),
                    "year": openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                    "players": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Items(type=openapi.TYPE_OBJECT)
                    ),
                },
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(type=openapi.TYPE_STRING)
                },
            ),
        },
    )
    def get(self, request):
        club = request.GET.get("club")
        year = request.GET.get("year")

        if not club:
            return Response({"error": "Missing 'club' parameter"}, status=status.HTTP_400_BAD_REQUEST)

        cache_key = f"club_players:{club}:{year or 'all'}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        queryset = Player.objects.filter(playerstatistics__club__icontains=club)

        if year:
            queryset = queryset.filter(playerstatistics__year=year)

        queryset = queryset.distinct().order_by("id")

        serializer = PlayerBasicSerializer(queryset, many=True)
        data = {
            "club": club,
            "year": year,
            "players": serializer.data,
        }
        cache.set(cache_key, data, timeout=3600)

        UserActivity.objects.create(
            user=request.user,
            action="searched_club_by_api",
            detail={"club": club, "year": year}
        )
        return Response(data)


class PlayersListAPI(ListAPIView):
    queryset = Player.objects.all().order_by("id")
    serializer_class = PlayerListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination

    @swagger_auto_schema(
        operation_description="Returns list with all players with short name and long name (with pagination).",
        manual_parameters=[
            openapi.Parameter(
                name="page",
                in_=openapi.IN_QUERY,
                description="Page number (default=1).",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name="page_size",
                in_=openapi.IN_QUERY,
                description="Page size (ex. 10, 20, 50).",
                type=openapi.TYPE_INTEGER
            ),
        ],
        responses={
            200: PlayerListSerializer(many=True),
        },
    )
    def get(self, request, *args, **kwargs):
        page_number = request.query_params.get("page", 1)
        page_size = request.query_params.get("page_size", 20)

        cache_key = f"players_list:page:{page_number}:size:{page_size}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        UserActivity.objects.create(
            user=request.user,
            action="viewed_players_list_by_api",
            detail={
                "page": page_number,
                "page_size": page_size,
            },
        )

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, 60 * 60 * 24)
        return response


class DashboardStatsAPI(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_description="Returns aggregated user activity statistics for the dashboard. Only accessible by admins.",
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "top_players_by_api": openapi.Schema(type=openapi.TYPE_ARRAY,
                                                         items=openapi.Items(type=openapi.TYPE_OBJECT)),
                    "top_players_by_website": openapi.Schema(type=openapi.TYPE_ARRAY,
                                                             items=openapi.Items(type=openapi.TYPE_OBJECT)),
                    "top_clubs_by_api": openapi.Schema(type=openapi.TYPE_ARRAY,
                                                       items=openapi.Items(type=openapi.TYPE_OBJECT)),
                    "players_list_views": openapi.Schema(type=openapi.TYPE_INTEGER),
                },
            )
        },
    )
    @method_decorator(cache_page(5 * 60))
    def get(self, request):
        top_players_by_api = (
            UserActivity.objects.filter(action="viewed_player_by_api")
            .values("detail__short_name")
            .annotate(count=Count("id"))
            .order_by("-count")[:10]
        )

        top_players_by_website = (
            UserActivity.objects.filter(action="viewed_player_by_website")
            .values("detail__short_name")
            .annotate(count=Count("id"))
            .order_by("-count")[:10]
        )

        top_clubs_by_api = (
            UserActivity.objects.filter(action="searched_club_by_api")
            .values("detail__club")
            .annotate(count=Count("id"))
            .order_by("-count")[:10]
        )

        players_list_usage = (
            UserActivity.objects.filter(action="viewed_players_list_by_api")
            .values("detail__page", "detail__page_size")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

        return Response({
            "top_players_by_api": list(top_players_by_api),
            "top_clubs_by_api": list(top_clubs_by_api),
            "top_players_by_website": list(top_players_by_website),
            "players_list_usage": list(players_list_usage),
        })


def change_number_format(number):
    units = ["", " K", " MLN"]
    k = 1000.0
    magnitude = int(floor(log(number, k)))
    return "%.3f%s" % (number / k ** magnitude, units[magnitude])
