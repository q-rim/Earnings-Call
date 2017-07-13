#! /usr/bin/python

# Author: Kyurim
# If webpage format changes, only update this.  Ensure the date returns in the following format: Feb 22, 2017

# to use, issue command followed by the ticker.  
# Example:
# command:	earnings_get_dates.py NFLX
# return:	Feb 22, 2017


from sys import argv
import sys
import subprocess
import time
import datetime


ticker = sys.argv[1]

CMD = 'lynx --dump https://finance.yahoo.com/calendar/earnings?symbol='+ticker+ \
	'    -useragent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/537.1 + \
	'' (KHTML, like Gecko) Chrome/21.0.1180.79 Safari/537.1 L_y_n_x/2.7"  | grep -A 3 "Showing Earnings for:" | tail -1'

# print CMD

p = subprocess.Popen(CMD, stdout=subprocess.PIPE, shell=True)
(output, err) = p.communicate()
# print output

word = output.split(" ")


# print word
# strip off the words until you get to the date
for w in word:
	if w in ["Jan", "Feb", "Mar", "Apr", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]:
		break;
	word = word[1:]
# print word

month = word[0]
date = word[1]
year = word[2]

print month + " " + date + " " + year[:4]

