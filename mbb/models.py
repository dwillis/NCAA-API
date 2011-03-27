from django.db import models
from django.template.defaultfilters import slugify
from decimal import *

class Team(models.Model):
    """
    Represents a college with a basketball team. The NCAA id is the one used by the 
    stats.ncaa.org site to denote a team. For example, Pittsburgh's id is 545.
    """    
    ncaa_id = models.IntegerField()
    name = models.CharField(max_length=125)
    slug = models.SlugField(max_length=125)
    
    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Team, self).save(*args, **kwargs)

    
class Season(models.Model):
    """
    Represents a single basketball season which spans two years. The NCAA id is the one used by the 
    stats.ncaa.org site to denote a season. For example, the 2010-11 season has an id of 10440.
    """
    season = models.CharField(max_length=7)
    start_year = models.IntegerField()
    end_year = models.IntegerField()
    ncaa_id = models.IntegerField()
    
    def __unicode__(self):
        return self.season

class TeamSeason(models.Model):
    """
    Represents a team during a particular season, along with information about that team. Since
    a team can change divisions from one season to the next, the division information is here, not
    in Team.
    """
    team = models.ForeignKey(Team)
    season = models.ForeignKey(Season)
    division = models.IntegerField()
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    minutes = models.IntegerField(default=0)
    field_goals_made = models.IntegerField(default=0)
    field_goals_attempted = models.IntegerField(default=0)
    field_goals_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.0'))
    three_point_fg_made = models.IntegerField(default=0)
    three_point_fg_attempted = models.IntegerField(default=0)
    three_point_fg_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.0'))
    free_throws_made = models.IntegerField(default=0)
    free_throws_attempted = models.IntegerField(default=0)
    free_throws_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.0'))
    points = models.IntegerField(default=0)
    scoring_average = models.DecimalField(max_digits=4, decimal_places=2, default=Decimal('0.0'))
    offensive_rebounds = models.IntegerField(default=0)
    defensive_rebounds = models.IntegerField(default=0)
    total_rebounds = models.IntegerField(default=0)
    rebounds_average = models.DecimalField(max_digits=4, decimal_places=2, default=Decimal('0.0'))
    assists = models.IntegerField(default=0)
    turnovers = models.IntegerField(default=0)
    steals = models.IntegerField(default=0)
    blocks = models.IntegerField(default=0)
    fouls = models.IntegerField(default=0)
    opp_field_goals_made = models.IntegerField(default=0)
    opp_field_goals_attempted = models.IntegerField(default=0)
    opp_field_goals_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.0'))
    opp_three_point_fg_made = models.IntegerField(default=0)
    opp_three_point_fg_attempted = models.IntegerField(default=0)
    opp_three_point_fg_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.0'))
    opp_free_throws_made = models.IntegerField(default=0)
    opp_free_throws_attempted = models.IntegerField(default=0)
    opp_free_throws_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.0'))
    opp_points = models.IntegerField(default=0)
    opp_scoring_average = models.DecimalField(max_digits=4, decimal_places=2, default=Decimal('0.0'))
    opp_offensive_rebounds = models.IntegerField(default=0)
    opp_defensive_rebounds = models.IntegerField(default=0)
    opp_total_rebounds = models.IntegerField(default=0)
    opp_rebounds_average = models.DecimalField(max_digits=4, decimal_places=2, default=Decimal('0.0'))
    opp_assists = models.IntegerField(default=0)
    opp_turnovers = models.IntegerField(default=0)
    opp_steals = models.IntegerField(default=0)
    opp_blocks = models.IntegerField(default=0)
    opp_fouls = models.IntegerField(default=0)
    
    def __unicode__(self):
        return u'%s in %s' % (self.team, self.season)
    
    def ncaa_url(self):
        return "http://stats.ncaa.org/team/index/%s?org_id=%s" % (self.season.ncaa_id, self.team.ncaa_id)
    

class Player(models.Model):
    """
    Represents a college basketball player as identified by the NCAA. The ncaa_id is the unique one used by 
    the stats.ncaa.org site. For example, Ashton Gibbs of Pittsburgh has an id of 904890.0, of which we only
    store the integer, since that's all that seems to matter.
    """
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    ncaa_id = models.IntegerField()
    
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Player, self).save(*args, **kwargs)

    
class PlayerSeason(models.Model):
    """
    Represents a college basketball player during a particular season. Since player information such as uniform
    number and year change from season to season, this information is retained here rather than in Player. The 
    height is broken into two fields to enable comparisons.
    """
    player = models.ForeignKey(Player)
    team_season = models.ForeignKey(TeamSeason)
    position = models.CharField(max_length=7)
    feet = models.IntegerField(default=0)
    inches = models.IntegerField(default=0)
    year = models.CharField(max_length=5, null=True)
    jersey = models.IntegerField(default=0)
    games_played = models.IntegerField(default=0)
    games_started = models.IntegerField(default=0)
    minutes = models.IntegerField(default=0)
    field_goals_made = models.IntegerField(default=0)
    field_goals_attempted = models.IntegerField(default=0)
    field_goals_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.0'))
    three_point_fg_made = models.IntegerField(default=0)
    three_point_fg_attempted = models.IntegerField(default=0)
    three_point_fg_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.0'))
    free_throws_made = models.IntegerField(default=0)
    free_throws_attempted = models.IntegerField(default=0)
    free_throws_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.0'))
    points = models.IntegerField(default=0)
    scoring_average = models.DecimalField(max_digits=4, decimal_places=2, default=Decimal('0.0'))
    offensive_rebounds = models.IntegerField(default=0)
    defensive_rebounds = models.IntegerField(default=0)
    total_rebounds = models.IntegerField(default=0)
    rebounds_average = models.DecimalField(max_digits=4, decimal_places=2, default=Decimal('0.0'))
    assists = models.IntegerField(default=0)
    turnovers = models.IntegerField(default=0)
    steals = models.IntegerField(default=0)
    blocks = models.IntegerField(default=0)
    fouls = models.IntegerField(default=0)
    double_doubles = models.IntegerField(default=0)
    triple_doubles = models.IntegerField(default=0)
    
    def __unicode__(self):
        return u'%s, %s' % (self.player, self.team_season)
    
    def height(self):
        return u'%s-%s' % (self.feet, self.inches)
    
    def ncaa_url(self):
        return "http://stats.ncaa.org/player?game_sport_year_ctl_id=%s&stats_player_seq=%s" % (self.team_season_id, self.player_id)
    
