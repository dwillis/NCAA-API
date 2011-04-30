from django.contrib import admin
from ncaa_api.mbb.models import Team, Season, TeamSeason, Player, PlayerSeason, Game

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

class GameAdmin(admin.ModelAdmin):
    list_display = ('home_team', 'home_team_score', 'visiting_team', 'visiting_team_score', 'datetime')

admin.site.register(Season, SeasonAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(TeamSeason, TeamSeasonAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(PlayerSeason, PlayerSeasonAdmin)
admin.site.register(Game, GameAdmin)