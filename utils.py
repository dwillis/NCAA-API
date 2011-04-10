import urllib
from BeautifulSoup import BeautifulSoup

def soupify(url):
    """
    Takes a url and returns parsed html via BeautifulSoup and urllib. Used by the scrapers.
    """
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html)
    return soup