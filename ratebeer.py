# -*- coding: utf-8 -*-
import sqlite3, re, requests, time, sys
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf8')

def levenshtein(a,b):
    "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a,b = b,a
        n,m = m,n

    current = range(n+1)
    for i in range(1,m+1):
        previous, current = current, [i]+[0]*n
        for j in range(1,n+1):
            add, delete = previous[j]+1, current[j-1]+1
            change = previous[j-1]
            if a[j-1] != b[i-1]:
                change = change + 1
            current[j] = min(add, delete, change)

    return current[n]

# Search on ratebeer
def ratebeer(searchstring, beername, breweryname):
    r = requests.post('http://www.ratebeer.com/findbeer.asp', data={'BeerName': searchstring})
    soup = BeautifulSoup(r.text, 'lxml')
    rb = soup.find_all('a', class_='rate')
    beers = []
    # Build collection of results
    for b in rb:
        rbid = re.findall('(\d+)', b['href'])[0]
        rbname = b.parent.previous_sibling('a')[0].text.strip()
        rbscore = b.parent.next_sibling.next_sibling.text.strip()
        rbratings = b.parent.next_sibling.next_sibling.next_sibling.text.strip()
        lev = levenshtein(rbname, "%s %s" % (breweryname, beername))
        beers.append((rbid, rbname, rbscore, rbratings, lev))
    return beers


conn = sqlite3.connect('beer.db')

conn.text_factory = str

c = conn.cursor()

c.execute("SELECT rowid, * FROM beers WHERE rbscore IS NULL OR rbscore = 0")
for row in c.fetchall():
    beerid = row[0]
    breweryid = row[3]
    beername = row[1]
    c.execute("SELECT name FROM breweries WHERE rowid = ?", (breweryid,))
    brewery = c.fetchone()[0]

    searchstring = '%s %s' % (beername, brewery)
    searchstring = searchstring.split()

    beers = []
    for i in range(0,len(searchstring)):
        ss = searchstring
        if i == 0: # Search for full string first.
            ss = " ".join(ss)
        else: # Then start chopping words off from the back
            ss = " ".join(ss[:i*-1])
        beers = ratebeer(ss, beername, brewery)

        if len(beers) > 0:
            print "Stopping at %d out of %d" % (i, len(searchstring))
            break

    if len(beers) == 0: # This probably won't ever happen..
        print "Found nothing for %s" % searchstring
        continue

    rb = sorted(beers, key=lambda beer: beer[4])[0] # Find best match according to lev

    soup = BeautifulSoup(requests.get('http://www.ratebeer.com/beer/%s/' % rb[0]).text)
    style = soup.find_all('a', href=re.compile('/beerstyles/.*/(\d+)/'))[0]
    stylename = style.text
    rbstyle = re.findall('(\d+)',style['href'])[0]

    rbweighed = soup.find_all('a', {'name': 'real average'})[0].text.split('/')[0].split(' ')[-1]
    
    c.execute("UPDATE beers SET rbid = ?, rbscore = ?, rbratings = ?, rbstyle = ?, rbweighed = ? WHERE rowid = ?", (rb[0], rb[2], rb[3], rbstyle, rbweighed, beerid))
    print "%s %s == %s: %s %s - %s" % (brewery, beername, rb[1], rb[2], rb[3], stylename) # Visual confirmation of match?
    conn.commit()
    time.sleep(1)

