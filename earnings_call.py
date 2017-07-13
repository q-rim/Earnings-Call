#! /usr/bin/python

# Author: Kyurim
# this program gives you alearts on Stock Market Earnings Call.  
# Automatically populates all data by scraping webpages based on your Stock Ticker input(Ticker.txt file).
# 1. emails notification to you @14, 7, and 1 day prior to the Earnings Call date.
# 2. automatically creates a webpage of Stock Market Earnings Call dates.  

# This file calls "earnings_get_dates.py <ticker>" which returns date in the following format:
# Jul 17, 2017

import subprocess
import time
import datetime

DIR = "./"			# set the working directory
MONTH = {"Jan":1, "Feb":2, "Mar":3, "Apr":4, "May":5, "Jun":6, "Jul":7, "Aug":8, "Sep":9, "Oct":10, "Nov":11, "Dec":12}
line_list = [];

def lynx_get_ticker_earnings_date(ticker_list):
	# Lynx text web-browser gets the dates of ticker.  Returns ['date Ticker1', 'date Ticker2' ...]
	txt = open(ticker_list ,'r')
	line=[]
	for ticker in txt:					# get line
		ticker = ticker[:len(ticker)-1];		#print ticker
		ticker_1st_char = ticker[0];			#print ticker_1st_char

		CMD = DIR + 'earnings_get_dates.py ' + ticker
		print CMD

		p = subprocess.Popen(CMD, stdout=subprocess.PIPE, shell=True)
		(output, err) = p.communicate()
		print output

		if output != "":				# handles the case where earnings_get_dates throws errors.
			date = output[:-1]; 		#print date
			print date
			line.append(date + "  " + ticker)
			print line

	txt.close()
	return line


def get_sorted_list_stock(line):
	# get sorted list of list of each stock: 
	#   Returns:  [ ['57', 'July', '20', '2015', 'NFLX'], ['58', 'July', '21', '2015', 'FB']]

	# put elements of line into a list:	
	#line_list=[]
	for i in range(len(line)):
		# print line[i]
		list_of_values = line[i].split();		#split into a list of values: ['July', '15,', '2015', 'GOOGL']
		#print list_of_values
		global line_list
		line_list.append(list_of_values)

	# strip trailing comma from date element
	for i in range(len(line_list)):
		line_list[i][1] = line_list[i][1][:-1]

	# prepend element:  number of days till earnings call date: 	['5', 'July', '15,', '2015', 'GOOGL']
	for i in range(len(line_list)):
		ll = line_list[i];				#print "ll:",ll
		year = int(ll[2]);				#print year
		month = MONTH[ll[0]];				#print month
		day = int(ll[1]);				#print day
		t_minus = days_to_earnings(year, month, day)
		line_list[i] = [t_minus] + ll;			#print "\nline_list:",line_list; # prepend T-minus date
		
	# sort line_list based on days till earnings call date.  Earliest to latest.
	line_list = sorted(line_list)
	return line_list	

def days_to_earnings(year, month, day):
	one_day = 86400 # sec
	cur_time = datetime.datetime.now(); 				#print "cur_time: ", cur_time
	cur_time_posix = time.mktime(cur_time.timetuple()); 		#print " - posix: ", cur_time_posix

	opt_time = datetime.datetime(year, month, day, 9, 0, 0, 0);	#print "opt_time: ", opt_time
	opt_time_posix = time.mktime(opt_time.timetuple());	 	#print " - posix: ", opt_time_posix;  

	t_minus = opt_time_posix - cur_time_posix;			#print "t-minus: ", t_minus; 	
	d_minus = int(t_minus) / int(one_day);				#print "d_minus: ", d_minus
	return d_minus


def create_index_html(sorted_list):
	# create html file
	wr_file = open(DIR + "index.html", 'w')

	head = 	'''
	<html>
	  <head>
	    <meta http-equiv="refresh" content="3600">
          <style>
             table, th, td {
                border: 1px solid black;
                border-collapse: collapse;
             }
          </style>
	  </head>
	  <body>
	    <h2>Quarterly Earnings Call Dates</h2>
	    <br />
            <table style="width:25%">
              <tr> <td><b>Ticker</b></td> <td><b>Earnings Call In</b></td> <td><b>Earnings Call Date</b></td> </tr>'''

	wr_file.write("%s\n" % head)

	# Update Timestamp
	t1 = datetime.datetime.now();	
	t1 = str(t1)[0:19];

	for l in sorted_list:
		m = l[1];		d = l[2];		y = l[3]; 		ticker = l[4];		t_m = str(l[0])
		mI=MONTH[m];	dI=int(d);		yI=int(y);		
		txt = '	       <tr> <td><a href="https://www.google.com/finance?q='+ticker+'">' +ticker+ '</a></td> '+ \
			'  <td align="right">'+t_m+' days</td>  '+ \
			'  <td align="right"><a href="https://finance.yahoo.com/calendar/earnings?symbol=' +ticker+ '">' + \
			 m +" "+ d +" "+ y +" "+'</a></td> </tr>' 

		# print txt
		wr_file.write("%s\n" % txt)

	tail = "	</table> <br /><p>Last updated:  " +t1+ "</p>"+'''
	  </body>
	</html>
	'''
	wr_file.write("%s\n" % tail)


def email_earnings_date(mailing_list):
	# email the option's list 10 days before the earnings release date.
	# create email text 
	outgoing_mail = False
	email_txt="http://www.your_website.com/earnings/\n\n\n"
	for l in line_list:
		t_minus = l[0];    t_m = str(l[0]);    m = l[1];    d = l[2];    y = l[3];    ticker = l[4];		
		#print '\n', t_minus, ticker 
		#if (t_minus<55) and (t_minus>0):			# used for testing
		#if True:
		if (t_minus==1) or (t_minus==7) or (t_minus==14):
			email_txt = email_txt + ticker + ' earnings call in '+t_m+ \
			' days.   (Earnings Call Date: ' +m+ ' ' +d+ ', ' +y+')\n';		#print email_txt
			outgoing_mail = True
	#t1 = datetime.datetime.now();
        #t1 = str(t1)[0:19];
	#eamil_txt = email_txt + t1

	# send email to mailing list
	if outgoing_mail == True:
		for email in mailing_list:
			CMD = 'echo "' +email_txt+ '" | mail -s "Earnings Call Notification" -a "From: Kyurim" ' +email
			#print CMD

			p = subprocess.Popen(CMD, stdout=subprocess.PIPE, shell=True)
			(output, err) = p.communicate()
			#print output

		print "mail sent to: ", mailing_list
	else:
		print "no mail sent"


# Main()
def main():
	# Lynx text web-browser gets the dates of ticker.  Returns [date Ticker]
	# line = lynx_get_ticker_earnings_date("/var/www/html/earnings/ticker.list");		#print "line:", line;	print; print 
	line = lynx_get_ticker_earnings_date(DIR + "ticker.list");		#print "line:", line;	print; print 

	# get sorted list of list of each stock:  
	#   Returns:  [ ['57', 'July', '20', '2015', 'NFLX'], ['58', 'July', '21', '2015', 'FB']]
	line_list = get_sorted_list_stock(line)
	#print line_list

	# create html file
	create_index_html(line_list)

	# email the option's list 10 days before the earnings release date.
	# mailing_list = ["jane@gmail.com", "bob@gmail.com", "john@gmail.com", "alice@gmail.com"]
	# email_earnings_date(mailing_list)


if __name__ == "__main__":
	main()
