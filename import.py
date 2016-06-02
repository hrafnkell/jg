# -*- coding: utf-8 -*-
import sqlite3, re, requests, time
from bs4 import BeautifulSoup

conn = sqlite3.connect('beer.db')

conn.text_factory = str

c = conn.cursor()
data = """1;Alesmith-002;Double Red IPA 650ml 8,5%; 2.554 
1;Alesmith-003;Speedway Stout - 12% - 750 ml; 3.667 
1;Alesmith-006;Decadence 2014 - 10% - 750 ml; 3.405 
2;Almanac-001;Farmers Reserve Cirtus 7% 375ml; 2.227 
3;amager-001;Hr. Frederiksen - 10,5% - 500ml; 1.392 
4;Anchorage-001;Bitter Monk - 750ml - 9%; 3.432 
4;Anchorage-002;Love Buzz Saison  - 750ml - 8%; 3.075 
4;Anchorage-003;Mosaic Saison  - 750ml - 6,5%; 2.609 
4;Anchorage-004;Whiteout Wit - 750ml - 6,5%; 2.609 
5;B.Nektar-005;Zombie Killer 5,5% - 500ml - cider; 1.572 
6;Bells-002;Kalamazoo Stout 6% 355ml; 733 
6;Bells-003;Java Stout 7,5% 355ml; 982 
6;Bells-004;Expedition Stout 10,5% 355ml; 1.244 
7;Brekeriet-002;Cassis 5,4% 750ml; 2.305 
7;Brekeriet-004;Zuur 5% 750ml; 1.703 
8;BREW-001;5 A.M. Saint 330ml. 5,0%; 472 
8;BREW-007;Sink the Bismarck 375ml. 41%; 14.251 
8;BREW-039;Dog B 330ml 15%; 2.271 
8;BREW-041;Dog C 330ml 15%; 2.580 
8;BREW-046;Abstrakt AB:17 - 375ml. 10,9%; 2.737 
8;BREW-047;Vagabond Pale ale gl.free 330ml 4,5%; 448 
8;BREW-049;Dog D imp stout 330ml 16,1%; 2.292 
8;BREW-053;Black Eyed King Imp stout 12,7% 330ml; 2.096 
9;crookedstave-001;Vielle Artisanal 4,2% 375 ml; 1.467 
9;crookedstave-002;St. Bretta (Autumn) 5,5% 375 ml; 1.572 
9;crookedstave-003;Vielle Artisanal (C&S) 4,2% 375 ml; 1.480 
9;crookedstave-006;Origins 6,5% 375 ml; 2.227 
9;crookedstave-007;Flor d'Lees 5% 375 ml; 2.148 
10;darkhorse-006;Tres Blueberry Stout 7,5% 355ml; 982 
11;demolen-001;Hemel & Aarde - 10% - 330ml; 1.297 
11;demolen-002;Tsarina Esra - 11% - 330ml; 1.336 
11;demolen-004;Rasputin Imperial Stout 10,4%; 1.310 
27;EvilTwin-006;Yin 10% 355ml; 927 
27;EvilTwin-035;Soft DK - imp. Stout 10,4% 355ml; 1.009 
12;founders-001;Dirty Bastard 355ml 8,5%; 650 
12;Founders-002;Centennial IPA 355ml 7,2%; 609 
12;Founders-002dós;Centennial IPA 355ml dós 7,2%; 499 
12;Founders-003;Porter 355ml 6,5%; 550 
12;Founders-004;All Day IPA 355ml 4,7%; 443 
12;Founders-004dós;All Day IPA 355ml dós 4,7%; 398 
12;Founders-005;Breakfast Stout 355ml 8,3%; 760 
12;Founders-006;Backwoods Bastard 355ml 11,6%; 1.120 
12;Founders-007;Imperial Stout 355ml 10,5%; 919 
12;Founders-011;Big Lushious 750ml 7,8%; 3.275 
12;Founders-012;Blushing Monk 750ml 9,2%; 3.536 
12;Founders-014;Rübæus  5,7% 355ml; 673 
12;Founders-015;Mango Magnifico 10% 750ml; 2.390 
12;Founders-016;Curmudgeon 9,8% 355ml; 917 
12;Founders-017;Mosaic Promise 355ml 5,5% ipa; 485 
12;Founders-018;Sumatra Mountain Brown  9,2% 355ml; 812 
13;JollyPumpkin-006;Fuego del Otoño saison 6,1% 750ml; 2.947 
14;Lervig-001;Pop That Cherry 750ml. 6,5%; 1.952 
14;Lervig-016;konrads stout - brewers reserve 10,4%; 917 
15;Logsdon-001;Seizoen Bretta 8% 750ml; 2.476 
15;Logsdon-002;Peche n'Brett 10% 750ml; 3.864 
15;Logsdon-003;Far West Vlaming 6,5% 750ml; 3.405 
15;Logsdon-007;Oak Aged Bretta 8,0% 750ml; 3.572 
15;Logsdon-008;Aberrant 8% 750ml; 2.301 
15;Logsdon-010;Szech´n brett 6,5% 750ml; 2.227 
16;LostAbbey-007;Carnevale 6,5% 750ml; 2.100 
16;LostAbbey-008;Serpents Stout 11% 750ml; 3.275 
16;LostAbbey-010;Avant Garde Ale 7% 750ml; 2.187 
16;LostAbbey-011;Devotion Ale blond 6,3% 750ml; 2.083 
16;LostAbbey-013;Angel's Share - Bourbon BA - 12,5% 375ml; 2.947 
16;LostAbbey-014;Track #10 - Imp.stout BA - 12% 375ml; 3.144 
17;MIK-001;American Dream 330ml. 4,6%; 617 
17;MIK-001glutenfree;American Dream Gluten Free 330ml. 4,6%; 603 
17;MIK-008;Green Gold 330ml. 7%; 749 
17;MIK-012;Wheat is the new Hop IPA 330ml. 6%; 719 
17;MIK-013BA;Beer Geek Breakfast Bourbon 330ml. 7,5%; 1.284 
17;MIK-018;Big Worse Barley Wine 12% 375ml; 1.572 
17;MIK-020;Funky E-star 330ml 9,39%; 917 
17;MIK-028;Black Hole Imp. Stout 375ml 13,1%; 1.605 
17;MIK-041;Hvedegoop w/ Three Floyds 750ml 10,4%; 2.401 
17;MIK-042;Mexas Ranger - 330ml 6,6%; 786 
17;MIK-044;BooGoop (W/ Three Floyds) 750ml 10,4%; 2.401 
17;MIK-046;Nelson Sauvignon 9% 750ml; 3.471 
17;MIK-053;Invasion IPA (w/Anchorage) 750ml. 8%; 3.185 
17;MIK-059;Hvad Såå!? wild ale 330ml. 6,8%; 794 
17;MIK-060;Beer Geek Brunch Weasel 10,9% 330ml; 1.362 
17;MIK-060Cognac;Beer Geek Brunch W.BA Cognac 10,9% 330ml; 1.834 
17;MIK-063;Beer Geek Vanilla Shake 330ml, 13%; 1.375 
17;MIK-068;French Oak Series 375ml 19,3%; 2.685 
17;MIK-071;U Alright 4,5% - 330ml; 571 
17;MIK-080;Hop Burn High  IIPA 10% - 330ml; 1.035 
17;MIK-083;Black - BA teq/spreyside ed. 18,8% 375ml; 3.037 
17;MIK-093;Spontancassis 7,7% - 375ml; 1.585 
17;MIK-094;Drakes: Jolly Rodger 650ml. 9,6%; 1.857 
17;MIK-103;Weyerbacher Tiny, 750ml 11,8%; 2.786 
17;MIK-108;Koppi Barley Wine 10% 330ml; 1.178 
17;MIK-136;Amass Crazy w/plum 5% 330ml; 1.364 
17;MIK-149;Frelser Trippelbock 11% 750ml; 2.331 
17;MIK-164;Blackest bourbon ba 17,12% 375ml; 2.423 
17;MIK-165;Grassroots Artic saison 6% 750ml; 3.091 
17;MIK-168;Black Ink & Blood BA bourbon 750ml 17,1%; 4.453 
17;MIK-169;Black Ink & Blood BA Brandy 750ml 17,1%; 4.453 
17;MIK-173;Beer Geek Dessert 330ml 11%; 1.264 
17;MIK-174;Spontandryhop Citra  5,5% 330ml; 884 
17;MIK-177;H. Vibskov : Den plettede gris 5% 330ml; 603 
17;MIK-198;Vesterbro Wit 4,5% 330ml; 570 
17;MIK-199;Hop On Drinkin Berlin 2,8% 330ml; 452 
17;MIK-202;Mad Beer Jerez Sherry 7,7% 375ml; 1.538 
17;MIK-203;Risgoop v/ Three floyds 10,4% 750ml; 2.401 
17;MIK-207;Spontanwatermelon 7,7% 375ml; 1.585 
17;MIK-210;Bone Dry Geuze w/Boon 7,0% 750ml; 2.489 
17;MIK-211;Tommi's Burger Joint 6% 330ml; 629 
17;MIK-215;Winale 8,1% 375ml; 1.834 
17;MIK-216;Acid Trip BA Red Wine  8,8% 375ml; 1.886 
17;MIK-217;Acid Trip BA White Wine  8,1% 375ml; 1.834 
17;MIK-218;Spontanpear  7,7% 375ml; 1.585 
17;MIK-219;Meirer Beer Geek Riesling  11% 750ml; 3.405 
17;MIK-221;Recipe 1000 BA Chardonnay  9% 375ml; 2.187 
17;MIK-222;Recipe 1000 BA Sauternes  9% 375ml; 2.187 
17;MIK-223;Spontanpineapple 7,7% 375ml; 1.663 
17;MIK-224;Stick in the Ear IPA 6,5% 330ml; 694 
17;MIK-225;Grassroots Arctic Soiree 6% 750ml; 3.091 
17;MIK-226;Spontandryhop Simcoe  5,5% 330ml; 884 
17;MIK-230;Nelson Sauvin 9% 750ml; 3.471 
17;MIK-230dryhopped;Nelson Sauvin dry hopped 9% 750ml; 3.733 
17;MIK-232;Chill Pils Orange 4,7% 330ml; 596 
17;MIK-233Cherry;Ich Bin Berliner Weisse 3,7% 500ml dós; 603 
17;MIK-233Peach;Ich Bin Berliner Weisse 3,7% 500ml dós; 603 
17;MIK-124;Blå Spögelse v/ Three floyds 7,7% 750ml; 3.467 
17;MIK-175;Spontandryhop Mosaic 5,5% 330ml; 865 
18;Omnipollo-001;Leon 6,5% 330ml; 714 
18;Omnipollo-002;Nebuchadnezzar 8,5% 330ml; 906 
18;Omnipollo-003;Mazarin 5,6% 330ml; 720 
18;Omnipollo-019;3 Protein IPA 8% 330ml; 930 
18;Omnipollo-022;Pineapple Gose 3,5% 330ml; 596 
18;Omnipollo-027;Noa Double Barrel 11% 330ml; 1.768 
18;Omnipollo-028;Bianca Blueberry 3,5% 330ml; 902 
19;OudBeersel-001;Gueze 375ml 6%; 899 
19;OudBeersel-001stór;Geuze 750ml 6%; 1.759 
19;OudBeersel-002;Kriek 375ml 6%; 998 
19;OudBeersel-003;Bzart Lambiek 2012 750ml 8%; 2.483 
19;OudBeersel-004;Bzartekenlambiek 2012 750ml 8%; 2.582 
28;pel-002;Saison Dupont 1/3 6,5%; 623 
20;pel-004;Trappist Rochefort 8 - 9,2%; 851 
20;pel-005;Trappist Rochefort 10° - 11,3%; 1.140 
21;pel-024;3 fonteinen Oudeek -375ml 6%; 1.755 
22;portbrewing-001ba;Santas Little Helper BA bourbon10% 375ml; 3.013 
22;portbrewing-002;Old Viscosity 10% 650ml; 2.220 
22;portbrewing-002ba;Older Viscosity 12% 375ml; 2.854 
23;Prairie-004;Prairie Ale 8,2% 500ml; 1.873 
23;Prairie-005;Prairie Hop 8% 500ml; 1.834 
23;Prairie-008;Brett C.  8,1% 500ml; 2.033 
23;Prairie-009;Prairie Gold  sour golden ale 7% 500ml; 1.946 
24;Surly-001;Brett Mikkels 7,5% 750ml; 2.449 
25;to-öl-001;Black Ball Porter 330ml 8%; 813 
25;to-öl-006;First Frontier IPA 330ml 7,1%; 761 
25;to-öl-010;Goliat Imp. Coffee stout - 375ml 10,1%; 1.388 
25;to-öl-010BA;Goliat Barrel Aged - 375ml 10,1%; 1.834 
25;to-öl-013;Dangerously Close To Stupi - 330ml 9,3 %; 982 
25;to-öl-018;Black Malts and Body Salts 9,9% - 330ml; 982 
25;to-öl-019;Fuck Art - This is Archtecture 5% 330ml; 596 
25;to-öl-042;Gossip Gose w/Rose Hip 330ml 4,3%; 557 
25;to-öl-050;Brewberry American strong 9,8% 330ml; 956 
25;to-öl-051;By Udder Means Milk stout 7% 330ml; 727 
25;to-öl-052;Long time no see imp.stout 12,8% 330ml; 1.470 
25;to-öl-054;Liquorice Confidence 14% 375ml; 1.669 
25;to-öl-070;Sur Simcoe sour session IPA 4,5% 330ml; 511 
25;to-öl-073;Sur Yule Sour pale w/cherries 5,4% 330ml; 629 
25;to-öl-074;Smoke on the Porter BA 13,4% 330ml; 2.096 
25;to-öl-075;My Pils 4% 500ml dós; 499 
25;to-öl-077;Berry White 5% 330ml; 714 
25;to-öl-079;Mr. Blue blueberry saison 7% 330ml; 864 
25;to-öl-080;Totem Pale Gluten free 2,2% 330ml; 373 
25;to-öl-081;Velvets Are Blue saison 5,5% 330ml; 714 
26;TopplingG-003;Rover Truck 6,6% 475ml dós; 969 """

d = []
for i in data.split('\n'):
	t = i.split(';')
	breweryid = t[0]
	name = t[2]
	ml = re.findall(r'(\d+) *ml', t[2], re.I)
	name = re.sub(r'(\d+) *ml', '', name)
	if not ml:
		ml = 0
	else:
		ml = ml[0]
	
	abv = re.findall(r'(\d+,*?\d*) *%', t[2])
	name = re.sub(r'(\d+,*?\d*) *%', '', name).replace(' -  -', '').strip()
	if not abv:
		abv = "0"
	else:
		abv = abv[0]
	abv = abv.replace(',', '.')

	t[3] = t[3].replace('.','')

	t[2] = name

	t = t + [ml, abv]

	d.append(t)

c.execute('delete from beers')
conn.commit()

c.executemany('INSERT INTO beers (brewery, stockid, name, price, size, abv) VALUES (?,?,?,?,?,?)', d)

conn.commit()
conn.close()
