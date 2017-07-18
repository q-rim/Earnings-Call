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
MONTHS_DICT = {"Jan":1 , "Feb":2, "Mar":3, "Apr":4, "May":5, "Jun":6, "Jul":7, "Aug":8, "Sep":9, "Oct":10, "Nov":11, "Dec":12}


def daysToEarnings(line):
	# arg (str):  takes in a line of command output
	# return (int):  days until earning

	# Get Dates
	word = line.split(" "); 		#print word
	# strip off the prepending words until you get to the date
	for w in word:
		if w in MONTHS_DICT:
			break;
		word = word[1:]
		print word
	# print word

	month = word[0]
	day = word[1]
	year = word[2]
	# print "month, day, year(str): ", month, day, year

	mm = int(MONTHS_DICT[month])
	dd = int(day[:-1])				# [:-1] strips off the trailing comma
	yyyy = int(year[:-1])			# [:-1] strips off the trailing comma
	# print "month, day, year(int): ", mm , dd, yyyy

	# convert earnings call date to epoch
	time_epoch_earn = datetime.datetime(yyyy, mm, dd).strftime("%s")
	# print "time_epoch_earn: ", time_epoch_earn, "\ttype:", type(time_epoch_earn)

	# current time in epoch
	curr_time = datetime.datetime.now(); 		#print "curr_time: ", curr_time, "\t type:", type(curr_time)
	cTime = curr_time.timetuple(); 				#print "cTime: ", cTime, "\ncTime type: ", type(cTime)
	#print cTime.tm_year, type(cTime.tm_year)	# get year example
	time_epoch_curr = datetime.datetime(cTime.tm_year, cTime.tm_mon, cTime.tm_mday).strftime("%s")
	# print "time_epoch_curr: ", time_epoch_curr, "\ttype:", type(time_epoch_curr)

	# time_earnings in days
	oneDay = 86400 # sec
	timeToEarnings = int(time_epoch_earn) - int(time_epoch_curr)
	daysToEarnings = timeToEarnings / oneDay
	print "daysToEarnings: " , daysToEarnings
	return daysToEarnings



CMD = 'lynx --dump https://finance.yahoo.com/calendar/earnings?symbol='+ticker+ \
	'    -useragent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/537.1 + \
	'' (KHTML, like Gecko) Chrome/21.0.1180.79 Safari/537.1 L_y_n_x/2.7"  | grep -A 3 "Showing Earnings for:" | tail -1'

# print CMD

p = subprocess.Popen(CMD, stdout=subprocess.PIPE, shell=True)
(output, err) = p.communicate()
print "CMD OUTPUT> ", output, "\ntype: ", type(output)



if daysToEarnings(output) > 90:
	print "not the right date - value greater than 3 mo"
else:
	print "earnings within 3 mo"
