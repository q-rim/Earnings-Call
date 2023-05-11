# earnings-call
earnings call notification

Functions of this application: 1. reads the ticker.list file to find the Ticker list. 2. for each ticker, looks up the earnings call date. 3. If the earnings call is in 1, 7, 14 days, it will send email to the email list.

To ensure that this application works, make sure that your linux server can send emails. Place all the following files in the /var/www/ directory. Files: 1. earnings_call.py - written in Python. Does all the work. 2. ticker.list - list of the tickers you want notification for. 3. index.html - place this file in the same directory. This file will get re-generated each time the earnings_call.py runs.

TESTING Github UI update.

Test2
