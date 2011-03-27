import urllib
from BeautifulSoup import BeautifulSoup
from django.utils.safestring import SafeUnicode
from ncaa_api.mbb.models import Season, Team, TeamSeason, Player, PlayerSeason

def team_parser(season_id=2011, division="1"):
    # defaults to division 1, but also supports division 3
    season = Season.objects.get(end_year=season_id)
    url = "http://stats.ncaa.org/team/inst_team_list/%s?division=%s" % (season.ncaa_id, division)
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html)
    team_links = [x.find('a') for x in soup.findAll('td')]
    for team in team_links:
        ncaa_id = int(team["href"].split("=")[1])
        name = SafeUnicode(team.contents[0])
        t, created = Team.objects.get_or_create(ncaa_id = ncaa_id, name = name)
        team_season, created = TeamSeason.objects.get_or_create(team=t, season=season, division=1)

def roster_parser(season_id, team_id, division=1):
    team_season = TeamSeason.objects.select_related().get(team__ncaa_id=team_id, season__end_year=season_id)
    url = "http://stats.ncaa.org/team/index/%s?org_id=%s" % (team_season.season.ncaa_id, team_id)
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html)
    rows = soup.findAll('table')[2].findAll('tr')
    player_links = rows[2:len(rows)]
    for p in player_links:
        ncaa_id = int(float(p.findAll('td')[1].find('a')['href'].split('=', 2)[2]))
        player, player_created = Player.objects.get_or_create(ncaa_id = ncaa_id)
        if player_created:
            last, first = [x.strip() for x in p.findAll('td')[1].find('a').contents[0].split(',')]
            player.name = first + u' '+ last
            player.save()
        player_season, ps_created = PlayerSeason.objects.get_or_create(player=player, team_season=team_season)
        if ps_created:
            player_season.jersey = int(p.findAll('td')[0].contents[0])
            try:
                player_season.position = SafeUnicode(p.findAll('td')[2].contents[0])
                player_season.feet = int(p.findAll('td')[3].contents[0].split('-')[0])
                player_season.inches = int(p.findAll('td')[3].contents[0].split('-')[1])
                player_season.year = SafeUnicode(p.findAll('td')[4].contents[0])
            except:
                pass
            player_season.save()

