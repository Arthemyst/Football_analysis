from django.core.cache import cache

def invalidate_players_cache():
    """
    Clears all players-related cache entries.
    """
    cache.delete_pattern("players_list:*")  # jeżeli używasz wersjonowanych kluczy
    cache.delete("dashboard_stats")
