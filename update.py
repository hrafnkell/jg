# -*- coding: utf-8 -*-
import sqlite3, re, requests, time
from bs4 import BeautifulSoup

conn = sqlite3.connect('beer.db')

conn.text_factory = str

c = conn.cursor()
fo = open('update.txt', 'rw+')
data = fo.readlines()
#data = """Alesmith-002;Dobule Red IPA 650ml 8,5%;2554
#to-öl-087;Ginie Gose 4,2% 330ml;563"""

d = []
for i in data:
	if len(i) < 5: # Ignore short lines.
		continue
	
	t = i.split(';')
	breweryid = t[0]
	name = t[2]
	ml = re.findall(r'(\d+) *ml', name, re.I)
	name = re.sub(r'(\d+) *ml', '', name)
	if not ml:
		ml = 0
	else:
		ml = ml[0]
	
	abv = re.findall(r'(\d+,*?\d*) *%', name)
	name = re.sub(r'(\d+,*?\d*) *%', '', name).replace(' -  -', '').strip()
	if not abv:
		abv = "0"
	else:
		abv = abv[0]
	abv = abv.replace(',', '.')

	# Remove dot from price, if necessary.
	t[3] = t[3].replace('.','')

	t[2] = name

	t = t + [ml, abv]

	d.append(t)

#c.execute('update beers set enabled = 0')
#conn.commit()

for b in d:
	c.execute("SELECT rowid, * FROM beers WHERE stockid = ?", (b[0],))
	row = c.fetchone()

	if row: # Update if exists
		c.execute('UPDATE beers SET name = ?, price = ?, enabled = 1 WHERE rowid = ?', (b[1], b[2], row[0]))
		d.remove(b)
	else: # Figure out brewery id?
		print "%s %s" % (b[0], b[1])
		#breweryid = input("Brewery ID: ")
		#b.insert(0,breweryid)
		c.execute('INSERT INTO beers (brewery, stockid, name, price, size, abv, enabled) VALUES (?,?,?,?,?,?,1)', b)

conn.commit()
conn.close()
