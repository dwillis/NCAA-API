import datetime
from dateutil.parser import *
from ncaa_api.utils import soupify
from django.utils.safestring import SafeUnicode
from ncaa_api.mbb.models import Game, Season, Team, TeamSeason, Player, PlayerSeason

def game_parser(id):
    url = "http://stats.ncaa.org/game/box_score/%s" % id
    soup = soupify(url)
    visit_id, home_id = [int(x['href'].split('=')[1]) for x in soup.findAll('table')[0].findAll('a')]
    visit = Team.objects.get(ncaa_id=visit_id)
    home = Team.objects.get(ncaa_id=home_id)
    game_details = soup.findAll('table')[2]
    dt = parse(game_details.findAll('td')[1].contents[0])
    loc = game_details.findAll('td')[3].contents[0]
    attend = int(game_details.findAll('td')[5].contents[0].replace(',',''))
    officials = soup.findAll('table')[3].findAll('td')[1].contents[0].strip()
    scores = soup.findAll('table')[0].findAll('td', attrs={'align':'right'})
    visit_team_scores = [int(x.renderContents()) for x in scores[0:len(scores)/2]]
    home_team_scores = [int(x.renderContents()) for x in scores[len(scores)/2:len(scores)]] # second team listed is considered home team
    game, created = Game.objects.get_or_create(ncaa_id=id, home_team=home, visiting_team=visit, datetime=dt, location=loc, attendance=attend, officials=officials, home_team_score=home_team_scores[(len(scores)/2)-1], visiting_team_score=visit_team_scores[(len(scores)/2)-1])

def team_parser(season_id=2011, division="1"):
    # defaults to division 1, but also supports division 3
    season = Season.objects.get(end_year=season_id)
    url = "http://stats.ncaa.org/team/inst_team_list/%s?division=%s" % (season.ncaa_id, division)
    soup = soupify(url)
    team_links = [x.find('a') for x in soup.findAll('td')]
    for team in team_links:
        ncaa_id = int(team["href"].split("=")[1])
        name = SafeUnicode(team.contents[0])
        t, created = Team.objects.get_or_create(ncaa_id = ncaa_id, name = name)
        team_season, created = TeamSeason.objects.get_or_create(team=t, season=season, division=1)

def roster_parser(season_id, team_id, division=1):
    team_season = TeamSeason.objects.select_related().get(team__ncaa_id=team_id, season__end_year=season_id)
    url = "http://stats.ncaa.org/team/index/%s?org_id=%s" % (team_season.season.ncaa_id, team_id)
    soup = soupify(url)
    rows = soup.findAll('table')[2].findAll('tr')
    player_links = rows[2:len(rows)]
    for p in player_links:
        try:
            ncaa_id = int(float(p.findAll('td')[1].find('a')['href'].split('=', 2)[2]))
            name = extract_player_name(p.findAll('td')[1].find('a').contents[0].split(','))
        except:
            ncaa_id = -1
            name = extract_player_name(p.findAll('td')[1].contents[0].split(','))
        player, player_created = Player.objects.get_or_create(name=name, ncaa_id = ncaa_id)
        player_season, ps_created = PlayerSeason.objects.get_or_create(player=player, team_season=team_season)
        if ps_created:
            try:
                player_season.jersey = int(p.findAll('td')[0].contents[0])
            except:
                player_season.jersey = None
            try:
                player_season.position = SafeUnicode(p.findAll('td')[2].contents[0])
                player_season.feet = int(p.findAll('td')[3].contents[0].split('-')[0])
                player_season.inches = int(p.findAll('td')[3].contents[0].split('-')[1])
                player_season.year = SafeUnicode(p.findAll('td')[4].contents[0])
            except:
                pass
            player_season.save()

def extract_player_name(name_text):
    try:
        last, first = [x.strip() for x in name_text]
        name = first + u' '+ last
    except ValueError:
        last, rest, first = [x.strip() for x in name_text]
        name = first + u' '+ last + u' '+ rest
    return name