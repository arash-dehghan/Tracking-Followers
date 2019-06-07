# Tracking Instagram Followers

This is code used with SQL databses to store and graph followers information for multiple instagram accounts. This is a pairing project with the Clout Creator project.

# How To Run

1) Create new python file
2) Copy the following code into file

import os

username = 'YOUR INSTAGRAM USERNAME' <br />
password = 'YOUR INSTAGRAM PASSWORD' <br />
accounts = 'accountone accounttwo accountthree' <br />
entervalues = 'n' #Should it enter in values into database? <br />
graphoverall = 'n' #Should it graph overall progress? <br />
graphdaily = 'n' #Should it graph daily progress? <br />

os.system(f'python3 Insta-Tracker.py -user {username} -pass {password} -acc {accounts} -e {entervalues} -og {graphoverall} -dg {graphdaily}')

3) Run code in file

