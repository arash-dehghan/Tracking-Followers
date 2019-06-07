from InstagramAPI import InstagramAPI
import sqlite3
import time
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import style
import random
import argparse
style.use('fivethirtyeight')

#### DATABASE SECTION ####
def GrabAccountIDs(list_of_accounts):
    list_of_account_ids = []

    for account in list_of_accounts:
        InstagramAPI.searchUsername(account)
        user = InstagramAPI.LastJson
        list_of_account_ids.append(user['user']['pk'])
    return list_of_account_ids

def create_table():
    conn = sqlite3.connect('FollowerCount.db')
    c = conn.cursor()
    #Upper case are SQL commands, could not capitalize it, but is then harder to read
    c.execute('CREATE TABLE IF NOT EXISTS FollowerCount(Datestamp TEXT, Account TEXT, Followers INTEGER, FollowersGained INTEGER)')
    c.close
    conn.close

def dynamic_data_entry(account_name, follower_count):
    conn = sqlite3.connect('FollowerCount.db')
    c = conn.cursor()
    #Setting the value of unix to time.time()
    #Unix time (also known as POSIX time or UNIX Epoch time) is a system for describing a point in time. It is the number of seconds that have elapsed since 00:00:00 Thursday, 1 January 1970, Coordinated Universal Time (UTC), minus leap seconds.
    unix = time.time()
    #We set date to a string value of the current date, in the below format of year-month-day hour:minutes:seconds
    date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H'))

    c.execute("SELECT COUNT(Followers) FROM FollowerCount WHERE Account=(?)", (account_name,))
    number_of_elements = c.fetchall()[0][0]
    if number_of_elements == 0:
        followers_gained = 0
    else:
        c.execute("SELECT Followers FROM FollowerCount WHERE Account =(?) ORDER BY Datestamp DESC LIMIT 1", (account_name,))
        followers_gained = follower_count - int(c.fetchall()[0][0])

    #Now we execute this and insert into our data base the data which we have, and we format it as is seen below
    c.execute("INSERT INTO FollowerCount (Datestamp, Account, Followers, FollowersGained) VALUES (?,?,?,?)", (date, account_name, follower_count,followers_gained))
    #We commit to save the changes to the database, we however don't close the connection and the cursor, since we will probably want to do this multiple times, and we don't want to waste time closing it each time only to have to re-open it. Check the bottom to see when we close it.
    conn.commit()

def enter_followers(mylist):

    conn = sqlite3.connect('FollowerCount.db')
    c = conn.cursor()
    create_table()
    for account in mylist:
        InstagramAPI.getUsernameInfo(account)
        user = InstagramAPI.LastJson
        account_followers = user['user']['follower_count']
        account_username = user['user']['username']
        dynamic_data_entry(account_username,account_followers)
    c.close
    conn.close



#### GRAPHING SECTION ####
def graph_follower_progress(accounts):
    conn = sqlite3.connect('FollowerCount.db')
    c = conn.cursor()

    values = []
    dates = []
    linestyles = ['-', '--', '-.', ':']

    for account in accounts:
        v = []
        c.execute('SELECT Datestamp,Followers FROM FollowerCount WHERE Account =(?) ', (account,))
        for value in c.fetchall():
            v.append(value[1])
            if account == accounts[0]:
                dates.append(value[0])
        values.append(v)

    for i in range(0,len(values)):
        plt.plot_date(dates,values[i], random.choice(linestyles), c = np.random.rand(3,))

    plt.title('Total Followers')
    plt.xlabel('Date')
    plt.ylabel('Followers')

    plt.legend(accounts, loc='upper left')

    plt.show()
    c.close
    conn.close

def graph_follower_gained_progress(accounts):
    conn = sqlite3.connect('FollowerCount.db')
    c = conn.cursor()

    values = []
    dates = []
    linestyles = ['-', '--', '-.', ':']

    for account in accounts:
        v = []
        c.execute('SELECT Datestamp,FollowersGained FROM FollowerCount WHERE Account =(?) ', (account,))
        for value in c.fetchall():
            v.append(value[1])
            if account == accounts[0]:
                dates.append(value[0])
        values.append(v)
    for i in range(0,len(values)):
        plt.plot_date(dates,values[i], random.choice(linestyles), c = np.random.rand(3,))

    plt.title('Total Followers')
    plt.xlabel('Date')
    plt.ylabel('Followers')

    plt.legend(accounts, loc='upper left')

    plt.show()
    c.close
    conn.close

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Track and graph your Instagram growth!')
    parser.add_argument('-user', '--username', type=str, help='Instagram username', required=True)
    parser.add_argument('-pass', '--password', type=str, help='Instagram password', required=True)
    parser.add_argument('-acc','--accounts', nargs='+', help='Accounts whose growth you want to track', required=True)
    parser.add_argument('-e', '--enter_values', type=str, default='n', help='Enter values into SQL database')
    parser.add_argument('-og', '--graph_overall', type=str, default='n', help='Graph overall follower growth')
    parser.add_argument('-dg', '--graph_daily', type=str, default='n', help='Graph daily follower growth')

    args = parser.parse_args()

    assert(len(args.accounts) != 0), "No accounts provided to graph. Empty list!"

    InstagramAPI = InstagramAPI(args.username, args.password)
    InstagramAPI.login()

    account_ids = GrabAccountIDs(args.accounts)

    if args.enter_values == 'y':
        enter_followers(account_ids)
        print("Entered values into database")
    if args.graph_overall == 'y':
        graph_follower_progress(args.accounts)
        print("Graphed overall follower progress")
    if args.graph_daily == 'y':
        graph_follower_gained_progress(args.accounts)
        print("Graphed daily follower progress")
