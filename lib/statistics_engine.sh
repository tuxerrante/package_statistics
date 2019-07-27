#!/bin/bash
# take a unique pkg list from the second column
#	awk '{print $2}' $1
# split on "," but not on / 
# 	egrep -o "[/a-zA-Z0-9_-]+"
# remove repetitions, case insensitive
# 	sort | uniq -cdi

awk '{print $2}' $1 | egrep -o "[/.a-zA-Z0-9_-]+" | sort | uniq -cdi | sort -nr | awk 'BEGIN{i=0} { if (i<10){ print $2 "\t\t" $1; i++;} }'

: '
RESPONSE ~ 27 sec for 6.040.275 lines

fonts/fonts-cns11643-pixmaps 110999
x11/papirus-icon-theme 69475
fonts/texlive-fonts-extra 65577
games/flightgear-data-base 62458
devel/piglit 49913
doc/trilinos-doc 49591
x11/obsidian-icon-theme 48829
games/widelands-data 34984
doc/libreoffice-dev-doc 33669
misc/moka-icon-theme 33326


real	0m27,901s
user	0m30,725s
'


