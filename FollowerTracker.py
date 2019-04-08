import sqlite3
import time
import datetime
import numpy as np
from instagram.client import InstagramAPI
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import style
style.use('fivethirtyeight')

#List of Instagram Accounts you want to plot
mylist = ['INSTAGRAM ACCOUNT USERNAME 1', 'INSTAGRAM ACCOUNT USERNAME 2', 'INSTAGRAM ACCOUNT USERNAME 3','INSTAGRAM ACCOUNT USERNAME 4']
InstaAccount = {}

#Create JSON objects of the Instagram accounts you want to plot. You will need to get their Access Token Number using the official Instagram API
#Copy and paste this Instagram Account object as many times as you'd like to create more accounts to plot
InstaAccount['INSTAGRAM ACCOUNT USERNAME 1'] = {
'UserName' : 'YOUR USERNAME FOR THIS ACCOUNT',
'Name' : 'ACCOUNT NAME',
'Access_TokenNum' : 'INSTAGRAM ACCOUNT ACCESS TOKEN',
'User_ID' : USER ID FOR ACCOUNT
}


def create_table():
    """
    Create our SQLite table, establish the connection, create our table variables we want to have, such as Account name, Followers, Followers Gained, etc.
    """
    conn = sqlite3.connect('FollowerCount.db')
    c = conn.cursor()
    #Upper case are SQL commands, could not capitalize it, but is then harder to read
    c.execute('CREATE TABLE IF NOT EXISTS FollowerCount(Datestamp TEXT, Account TEXT, Followers INTEGER, FollowersGained INTEGER)')
    c.close
    conn.close

def dynamic_data_entry(account_name, follower_count):
    """
    Update the data we gathered into the SQLite Database dynamically
    """
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

def enter_followers():
    """
    Enter information into our database
    """
    conn = sqlite3.connect('FollowerCount.db')
    c = conn.cursor()
    create_table()

    for account in mylist:
        token = InstaAccount[account]['Access_TokenNum']
        api = InstagramAPI(access_token = token)
        user_info = api.user(InstaAccount[account]['User_ID'])
        number_of_followers = user_info.counts['followed_by']
        #print(InstaAccount[account]['UserName'] + ' : ' + str(number_of_followers))
        dynamic_data_entry(InstaAccount[account]['UserName'],number_of_followers)

    c.close
    conn.close

def graph_follower_progress():
    """
    Graph the followers count for each of our accounts based on the SQL data
    """
    conn = sqlite3.connect('FollowerCount.db')
    c = conn.cursor()

    fortnite_values = []
    reddead_values = []
    minecraft_values = []
    apex_values = []
    dates = []
    apex_dates = []

    c.execute('SELECT Datestamp,Followers FROM FollowerCount WHERE Account = "FortniteClipsXX" ')
    for value in c.fetchall():
        dates.append(value[0])
        fortnite_values.append(value[1])
    c.execute('SELECT Followers FROM FollowerCount WHERE Account = "RedDeadClipsXX" ')
    for value in c.fetchall():
        reddead_values.append(value[0])
    c.execute('SELECT Followers FROM FollowerCount WHERE Account = "BestOfMinecraftXX" ')
    for value in c.fetchall():
        minecraft_values.append(value[0])
    c.execute('SELECT Datestamp,Followers FROM FollowerCount WHERE Account = "ApexClipsXX" ')
    for value in c.fetchall():
        apex_dates.append(value[0])
        apex_values.append(value[1])
    #Plot the 'dates' values as the x-axis, the 'values' values as the y-axis, and set the line to be formatted like '-'
    plt.plot_date(dates,fortnite_values, ':', color = 'b')
    plt.plot_date(dates,reddead_values, '--', color = 'r')
    plt.plot_date(dates,minecraft_values, '-', color = 'g')
    plt.plot_date(apex_dates,apex_values, '-.', color = 'y')

    plt.title('Total Followers')
    plt.xlabel('Date')
    plt.ylabel('Followers')


    plt.legend(['Fortnite', 'Red Dead 2', 'Minecraft','Apex Legends'], loc='upper left')
    #Show the plot
    plt.show()

    c.close
    conn.close

def graph_follower_gained_progress():
    """
    Graph the followers gained for each of our accounts based on the SQL data
    """
    conn = sqlite3.connect('FollowerCount.db')
    c = conn.cursor()

    fortnite_values = []
    reddead_values = []
    minecraft_values = []
    apex_values = []
    dates = []
    apex_dates = []

    c.execute('SELECT Datestamp,FollowersGained FROM FollowerCount WHERE Account = "FortniteClipsXX" ')
    for value in c.fetchall():
        dates.append(value[0])
        fortnite_values.append(value[1])
    c.execute('SELECT FollowersGained FROM FollowerCount WHERE Account = "RedDeadClipsXX" ')
    for value in c.fetchall():
        reddead_values.append(value[0])
    c.execute('SELECT FollowersGained FROM FollowerCount WHERE Account = "BestOfMinecraftXX" ')
    for value in c.fetchall():
        minecraft_values.append(value[0])
    c.execute('SELECT Datestamp,FollowersGained FROM FollowerCount WHERE Account = "ApexClipsXX" ')
    for value in c.fetchall():
        apex_dates.append(value[0])
        apex_values.append(value[1])
    #Plot the 'dates' values as the x-axis, the 'values' values as the y-axis, and set the line to be formatted like '-'
    plt.plot_date(dates,np.array(fortnite_values), ':', color = 'b')
    plt.plot_date(dates,np.array(reddead_values), '--', color = 'r')
    plt.plot_date(dates,np.array(minecraft_values), '-', color = 'g')
    plt.plot_date(apex_dates,np.array(apex_values), '-.', color = 'y')

    plt.title('Followers Gained')
    plt.xlabel('Date')
    plt.ylabel('Followers')

    plt.legend(['Fortnite', 'Red Dead 2', 'Minecraft', 'Apex Legends'], loc='upper left')
    #Show the plot
    plt.show()

    c.close
    conn.close

"""
Run enter_followers() to enter in follower inforamtion for each of our accounts
graph_follower_gained_progress() to graph followers gained since last entry of data
graph_follower_progress() to graph followers count
"""
# enter_followers()
# graph_follower_gained_progress()
# graph_follower_progress()
