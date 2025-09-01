from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class PlayersListThrottle(UserRateThrottle):
    scope = "players_list"

class PlayerDetailThrottle(UserRateThrottle):
    scope = "player_detail"

class ClubPlayersThrottle(UserRateThrottle):
    scope = "club_players"

class DashboardThrottle(UserRateThrottle):
    scope = "dashboard"

class AnonAPIRateThrottle(AnonRateThrottle):
    scope = "anon_api"
