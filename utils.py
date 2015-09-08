import requests
from BeautifulSoup import BeautifulSoup
from mbb.models import Season, Team

def soupify(url):
    """
    Takes a url and returns parsed html via BeautifulSoup and urllib. Used by the scrapers.
    """
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html)
    return soup


def create_initial_seasons():
    twenty_eleven = Season.objects.create(season='2010-11', start_year=2010, end_year=2011, ncaa_id=10440)
    twenty_ten = Season.objects.create(season='2009-10', start_year=2009, end_year=2010, ncaa_id=10260)
