from django.contrib import admin

from .models import Player, PlayerStatistics, UserActivity

admin.site.register(Player)
admin.site.register(PlayerStatistics)
admin.site.register(UserActivity)
