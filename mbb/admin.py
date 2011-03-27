from django.contrib import admin
from ncaa_api.mbb.models import Team, Season, TeamSeason, Player, PlayerSeason

class SeasonAdmin(admin.ModelAdmin):
    list_display = ('season', 'start_year', 'end_year', 'ncaa_id')

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'ncaa_id')

class TeamSeasonAdmin(admin.ModelAdmin):
    pass

class PlayerAdmin(admin.ModelAdmin):
    pass

class PlayerSeasonAdmin(admin.ModelAdmin):
    list_display = ('player', 'team_season', 'position', 'year')

admin.site.register(Season, SeasonAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(TeamSeason, TeamSeasonAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(PlayerSeason, PlayerSeasonAdmin)