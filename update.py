# -*- coding: utf-8 -*-
import sqlite3, re, requests, time
from bs4 import BeautifulSoup

conn = sqlite3.connect('beer.db')

conn.text_factory = str

c = conn.cursor()
data = """Alesmith-002;Dobule Red IPA 650ml 8,5%;2554
Alesmith-003;Speedway Stout - 12% - 750 ml;3667
Alesmith-006;Decadence 2014 - 10% - 750 ml;3405
Almanac-001;Farmers Reserve Cirtus 7% 375ml;2227
amager-001;Hr. Frederiksen - 10,5% - 500ml;1392
Anchorage-001;Bitter Monk - 750ml - 9%;3432
Anchorage-002;Love Buzz Saison  - 750ml - 8%;3075
Anchorage-003;Mosaic Saison  - 750ml - 6,5%;2609
Anchorage-004;Whiteout Wit - 750ml - 6,5%;2609
B.Nektar-005;Zombie Killer 5,5% - 500ml - cider;1572
Bells-002;Kalamazoo Stout 6% 355ml;733
Bells-003;Java Stout 7,5% 355ml;982
Bells-004;Expedition Stout 10,5% 355ml;1244
Brekeriet-002;Cassis 5,4% 750ml;2305
Brekeriet-004;Zuur 5% 750ml;1703
BREW-002;Punk IPA 330ml. 5,6%;525
BREW-002dos;Punk IPA í dós 330ml. 5,6%;478
BREW-021;Nanny State 330ml. 0,5%;330
BREW-032;Jack Hammer IPA - 330ml 7,2%;665
BREW-032dós;Jack Hammer IPA - 330ml dós 7,2%;596
BREW-039;Dog B 330ml 15%;2271
BREW-041;Dog C 330ml 15%;2580
BREW-046;Abstrakt AB:17 - 375ml. 10,9%;2737
BREW-047;Vagabond Pale ale gl.free 330ml 4,5%;448
BREW-048;Hop Fiction 330ml 5,2%;491
BREW-049;Dog D imp stout 330ml 16,1%;2292
BREW-051;Paradox Compass Box 15%  330ml;2747
BREW-056;Elvis Juice V2.0  6,5% 330ml dós;549
BREW-060;Shipwreck w/ Ballast Point 13% 330ml;2096
crookedstave-001;Vielle Artisanal 4,2% 375 ml;1467
crookedstave-002;St. Bretta (Autumn) 5,5% 375 ml;1572
crookedstave-003;Vielle Artisanal (C&S) 4,2% 375 ml;1480
crookedstave-004;Surette 6,2% 375 ml;1585
crookedstave-005;Nightmare on Brett 9,7% 375 ml;1925
crookedstave-006;Origins 6,5% 375 ml;2227
crookedstave-007;Flor d'Lees 5% 375 ml;2148
darkhorse-006;Tres Blueberry Stout 7,5% 355ml;982
demolen-001;Hemel & Aarde - 10% - 330ml;1297
demolen-002;Tsarina Esra - 11% - 330ml;1336
demolen-004;Rasputin Imperial Stout 10,4%;1310
Dugges-004;Tropic Thunder 4,5% 330ml;650
Dugges-005;Tropic Sunrise 4,5% 330ml;707
Dugges-006;Vanilla Oak 10% 330ml;1349
Dugges-007;Coco Nut 10% 330ml;1349
EvilTwin-006;Yin 10% 355ml;927
EvilTwin-035;Soft DK - imp. Stout 10,4% 355ml;1009
founders-001;Dirty Bastard 355ml 8,5%;650
Founders-002;Centennial IPA 355ml 7,2%;609
Founders-002dós;Centennial IPA 355ml dós 7,2%;499
Founders-003;Porter 355ml 6,5%;550
Founders-004;All Day IPA 355ml 4,7%;443
Founders-004dós;All Day IPA 355ml dós 4,7%;398
Founders-005;Breakfast Stout 355ml 8,3%;760
Founders-006;Backwoods Bastard 355ml 11,6%;1120
Founders-007;Imperial Stout 355ml 10,5%;919
Founders-011;Big Lushious 750ml 7,8%;3275
Founders-012;Blushing Monk 750ml 9,2%;3536
Founders-014;Rübæus  5,7% 355ml;673
Founders-015;Mango Magnifico 10% 750ml;2620
Founders-016;Curmudgeon 9,8% 355ml;917
Founders-017;Mosaic Promise 355ml 5,5% ipa;485
Founders-018;Sumatra Mountain Brown  9,2% 355ml;812
Founders-020;Devil Dancer triple IPA 12% 355ml;1546
HoppinFrog-001;B.O.R.I.S. the Crusher 9,4% 650ml;2593
HoppinFrog-002;D.O.R.I.S. the Destroyer 10,5% 650ml;2986
JollyPumpkin-002;Maracaibo Especial 7,5% 750ml;3130
JollyPumpkin-004;Bam Noire 4,3% 750ml;2043
JollyPumpkin-006;Fuego del Otoño saison 6,1% 750ml;2947
Lervig-001;Pop That Cherry 750ml. 6,5%;1952
Lervig-016;konrads stout - brewers reserve 10,4%;917
Logsdon-001;Seizoen Bretta 8% 750ml;2476
Logsdon-001lítl;Seizoen Bretta 8% 375ml;1357
Logsdon-002;Peche n'Brett 10% 750ml;3864
Logsdon-003;Far West Vlaming 6,5% 750ml;3405
Logsdon-006;Cerasus 8,5% 750ml;3627
Logsdon-007;Oak Aged Bretta 8,0% 750ml;3572
Logsdon-008;Aberrant 8% 750ml;2301
Logsdon-010;Szech´n brett 6,5% 750ml;2227
LostAbbey-007;Carnevale 6,5% 750ml;2100
LostAbbey-008;Serpents Stout 11% 750ml;3275
LostAbbey-010;Avant Garde Ale 7% 750ml;2187
LostAbbey-011;Devotion Ale blond 6,3% 750ml;2083
LostAbbey-013;Angel's Share - Bourbon BA - 12,5% 375ml;2947
LostAbbey-014;Track #10 - Imp.stout BA - 12% 375ml;3144
MIK-001;American Dream 330ml. 4,6%;617
MIK-001glutenfree;American Dream Gluten Free 330ml. 4,6%;603
MIK-006;Koppi IPA 330ml. 6,9%;709
MIK-008;Green Gold 330ml. 7%;749
MIK-012;Wheat is the new Hop IPA 330ml. 6%;719
MIK-013BA;Beer Geek Breakfast Bourbon 330ml. 7,5%;1284
MIK-018;Big Worse Barley Wine 12% 375ml;1572
MIK-020;Funky E-star 330ml 9,39%;917
MIK-028;Black Hole Imp. Stout 375ml 13,1%;1605
MIK-031BA;It's Alive! White Wine BA 375ml. 8%;1656
MIK-037;Porter (imp. porter) 330ml 7,4%;786
MIK-041;Hvedegoop w/ Three Floyds 750ml 10,4%;2401
MIK-042;Mexas Ranger - 330ml 6,6%;786
MIK-044;BooGoop (W/ Three Floyds) 750ml 10,4%;2401
MIK-046;Nelson Sauvignon 9% 750ml;3471
MIK-053;Invasion IPA (w/Anchorage) 750ml. 8%;3185
MIK-059;Hvad Såå!? wild ale 330ml. 6,8%;794
MIK-060;Beer Geek Brunch Weasel 10,9% 330ml;1362
MIK-060Cognac;Beer Geek Brunch W.BA Cognac 10,9% 330ml;1834
MIK-063;Beer Geek Vanilla Shake 330ml, 13%;1375
MIK-068;French Oak Series 375ml 19,3%;2685
MIK-071;U Alright 4,5% - 330ml;571
MIK-075;Simcoe Dry Hopped Vodka 44% - 700ml;9824
MIK-076;Mikkeller Gin 44% - 700ml;10740
MIK-077;White Dog GIN 42% - 350ml;9280
MIK-080;Hop Burn High  IIPA 10% - 330ml;1035
MIK-083;Black - BA teq/spreyside ed. 18,8% 375ml;3037
MIK-093;Spontancassis 7,7% - 375ml;1585
MIK-094;Drakes: Jolly Rodger 650ml. 9,6%;1857
MIK-103;Weyerbacher Tiny, 750ml 11,8%;2786
MIK-108;Koppi Barley Wine 10% 330ml;1178
MIK-124;Blå Spögelse v/ Three floyds 7,7% 750ml;3467
MIK-136;Amass Crazy w/plum 5% 330ml;1364
MIK-149;Frelser Trippelbock 11% 750ml;2331
MIK-164;Blackest bourbon ba 17,12% 375ml;2423
MIK-165;Grassroots Artic saison 6% 750ml;3091
MIK-168;Black Ink & Blood BA bourbon 750ml 17,1%;4453
MIK-169;Black Ink & Blood BA Brandy 750ml 17,1%;4453
MIK-173;Beer Geek Dessert 330ml 11%;1264
MIK-174;Spontandryhop Citra  5,5% 330ml;884
MIK-175;Spontandryhop Mosaic 5,5% 330ml;864
MIK-178;Deception Session IPA 5% 330ml;603
MIK-197;Sort Kaffe 9,2% 330ml;969
MIK-198;Vesterbro Wit 4,5% 330ml;570
MIK-199;Hop On Drinkin Berlin 2,8% 330ml;452
MIK-202;Mad Beer Jerez Sherry 7,7% 375ml;1538
MIK-203;Risgoop v/ Three floyds 10,4% 750ml;1532
MIK-210;Bone Dry Geuze w/Boon 7,0% 750ml;2489
MIK-211;Tommi's Burger Joint 6% 330ml;629
MIK-215;Winale 8,1% 375ml;1834
MIK-216;Acid Trip BA Red Wine  8,8% 375ml;1886
MIK-217;Acid Trip BA White Wine  8,1% 375ml;1834
MIK-218;Spontanpear  7,7% 375ml;1585
MIK-219;Meirer Beer Geek Riesling  11% 750ml;3405
MIK-221;Recipe 1000 BA Chardonnay  9% 375ml;2187
MIK-222;Recipe 1000 BA Sauternes  9% 375ml;2187
MIK-223;Spontanpineapple 7,7% 375ml;1663
MIK-224;Stick in the Ear IPA 6,5% 330ml;694
MIK-225;Grassroots Arctic Soiree 6% 750ml;3091
MIK-226;Spontandryhop Simcoe  5,5% 330ml;884
MIK-230;Nelson Sauvin 9% 750ml;3471
MIK-230dryhopped;Nelson Sauvin dry hopped 9% 750ml;3209
MIK-232;Chill Pils Orange 4,7% 330ml;596
MIK-233Cherry;Ich Bin Berliner Weisse 3,7% 500ml dós;603
MIK-233Peach;Ich Bin Berliner Weisse 3,7% 500ml dós;603
MIK-234;Polly 2 6,2% 750ml;2423
MIK-235;Spontannelsonsauvin 5,5% 750ml;2489
MIK-236;Spontanyuzu 7,7% 375ml;1572
MIK-237;Stella 7 -  7% 750ml;2489
MIK-238;Black Bourbon 43% - 350ml;11395
Omnipollo-001;Leon 6,5% 330ml;714
Omnipollo-002;Nebuchadnezzar 8,5% 330ml;906
Omnipollo-003;Mazarin 5,6% 330ml;720
Omnipollo-004;Zodiak 6,2% 330ml;694
Omnipollo-022;Pineapple Gose 3,5% 330ml;596
Omnipollo-025;Bianca Raspberry 3,5% 330ml;799
Omnipollo-027;Noa Double Barrel 11% 330ml;1768
Omnipollo-028;Bianca Blueberry 3,5% 330ml;914
OudBeersel-001;Gueze 375ml 6%;899
OudBeersel-001stór;Geuze 750ml 6%;1759
OudBeersel-002;Kriek 375ml 6%;998
pel-002;Saison Dupont 1/3 6,5%;623
pel-003;Tripel Karmeliet 1/3 8,4%;821
pel-004;Trappist Rochefort 8 - 9,2%;851
pel-005;Trappist Rochefort 10° - 11,3%;1140
pel-024;3 fonteinen Oude Kriek -375ml 6%;1755
portbrewing-001ba;Santas Little Helper BA bourbon10% 375ml;3013
portbrewing-002;Old Viscosity 10% 650ml;2220
portbrewing-002ba;Older Viscosity 12% 375ml;2854
Prairie-004;Prairie Ale 8,2% 500ml;1873
Prairie-005;Prairie Hop 8% 500ml;1834
Prairie-008;Brett C.  8,1% 500ml;2033
Prairie-009;Prairie Gold  sour golden ale 7% 500ml;1946
rogue-014;Spruce Gin 750ml 45%;10730
rogue-020;Dead Guy Whiskey 750ml 40%;10620
rogue-021;Rouge Hazelnut Rum 750ml 40%;9782
rogue-022;Oregon Single Malt 750ml 40%;11852
rogue-023;Russian Imperial Stout 11,6% 750ml;3687
rogue-024;Rogue Double Chocolate Stout 8,7% 750ml;2620
Surly-001;Brett Mikkels 7,5% 750ml;2449
to-öl-001;Black Ball Porter 330ml 8%;813
to-öl-006;First Frontier IPA 330ml 7,1%;761
to-öl-010;Goliat Imp. Coffee stout - 375ml 10,1%;1388
to-öl-013;Dangerously Close To Stupi - 330ml 9,3 %;982
to-öl-017;Snowball Saison - To Öl - 330ml 8%;737
to-öl-018;Black Malts and Body Salts 9,9% - 330ml;982
to-öl-019;Fuck Art - This is Archtecture 5% 330ml;596
to-öl-038;The heathens are coming - 330ml - 5,4%;616
to-öl-041;Mine is Bigger Than Yours 375ml -12,5%;1506
to-öl-042;Gossip Gose w/Rose Hip 330ml 4,3%;557
to-öl-049;Thirsty Frontier -session IPA 4,5% 330ml;599
to-öl-050;Brewberry American strong 9,8% 330ml;956
to-öl-051;By Udder Means Milk stout 7% 330ml;727
to-öl-052;Long time no see imp.stout 12,8% 330ml;1470
to-öl-054;Liquorice Confidence 14% 375ml;1669
to-öl-070;Sur Simcoe sour session IPA 4,5% 330ml;511
to-öl-072;HundelufterBajer sessin ipa 5% 330ml;583
to-öl-073;Sur Yule Sour pale w/cherries 5,4% 330ml;629
to-öl-074;Smoke on the Porter BA 13,4% 330ml;2096
to-öl-075;My Pils 4% 500ml dós;499
to-öl-077;Berry White 5% 330ml;714
to-öl-080;Totem Pale Gluten free 2,2% 330ml;373
to-öl-081;Velvets Are Blue saison 5,5% 330ml;714
to-öl-085;Roses are brett 6% 330ml;825
to-öl-087;Ginie Gose 4,2% 330ml;563"""

d = []
for i in data.split('\n'):
	t = i.split(';')
	#breweryid = t[0]
	name = t[1]
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
	t[2] = t[2].replace('.','')

	t[1] = name

	t = t + [ml, abv]

	d.append(t)

c.execute('update beers set enabled = 0')
#conn.commit()

for b in d:
	c.execute("SELECT rowid, * FROM beers WHERE stockid = ?", (b[0],))
	row = c.fetchone()

	if row: # Update if exists
		c.execute('UPDATE beers SET name = ?, price = ?, enabled = 1 WHERE rowid = ?', (b[1], b[2], row[0]))
		d.remove(b)
	else: # Figure out brewery id?
		print "%s %s" % (b[0], b[1])
		breweryid = input("Brewery ID: ")
		b.insert(0,breweryid)
		c.execute('INSERT INTO beers (brewery, stockid, name, price, size, abv, enabled) VALUES (?,?,?,?,?,?,1)', b)

conn.commit()
conn.close()
