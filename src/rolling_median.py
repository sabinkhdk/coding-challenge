'''
Insight Data Engineering Fellowship coding challenge

@author: mr.sabinkhadka@gmail.com

Written and tested in python 2.7

This code needs two argument files: input text file with venmo transaction json file
and ouput text file to store rolling median

Date : 07/14/2016
'''
######################################################
# Import libraries
import sys, time, json
import networkx as nx
import sqlite3
import numpy as np
from datetime import datetime                   # for time conversion
######################################################
# Make sure the arguments files are read properly
if len(sys.argv) < 3:
    print 'Not sufficient arguments'
    print 'Please try again'
    sys.exit(0)
else:
    try:
        open(sys.argv[1], 'r')
    except:
        print 'cannot open the file'
        print 'please choose valid file'
        sys.exit(0)

ifile = sys.argv[1]   # Input tweet json file 
dfile = sys.argv[2]   # save median degrees in a file
#######################################################
# Function to parse json files
# Return actor, target and transaction datetime
def cleanInfo(jline):
    """
    Parse json line from the transaction
    input: json line
    return: actor, target time
    """
    prs_jsn = json.loads(jline)
    actor   = prs_jsn['actor']
    target  = prs_jsn['target']
    date    = prs_jsn['created_time']
    return [actor, target, date]
########################################################
# Create a database. Store data in a table 
db = sqlite3.connect('DataInfo.db')  # Create sql data base 
c  = db.cursor()  # for cursor pointer
try:
    c.execute('DROP TABLE IF EXISTS users')
    c.execute('''CREATE TABLE users(actor text, target text, 
                    date datetime default current_timestamp,
                    newTdate datetime,
                    diff float)''')
except:
    pass
########################################################
with open(ifile,'r') as f0, open(dfile,'w+') as f1:
    for f in f0:
        f = f.strip()
        cleanf = cleanInfo(f)
        n1_ = cleanf[0]   # actor
        n2_ = cleanf[1]   # target
        if cleanf[2]:
            cTime = time.strptime(cleanf[2], '%Y-%m-%dT%H:%M:%SZ')
            n3_ = datetime.fromtimestamp(time.mktime(cTime))  # datetime of transaction
        else:
            n3_ = ""
        if not n1_ or not n2_ or not n3_:
            pass
        else:
            c.execute('''INSERT INTO users (actor, target, date) VALUES (?, ?, ?) ''', (n1_, n2_, n3_))
            c.execute('''UPDATE users SET 'diff' = 
                            (SELECT strftime('%s' ,max(date)) FROM users) 
                            - strftime('%s',date)''')  # Calculate time difference in seconds
            c.execute('''DELETE FROM users WHERE diff > 60.00 ''')  # Maintain 60 secs window
            c.execute(''' SELECT actor, target FROM users ''')
            output = c.fetchall()
            g = nx.Graph()
            g.add_edges_from(output)
            deg = g.degree()
            mdn = np.median(deg.values())
            mn  = np.mean(deg.values())
            f1.write(str('%.2f')%mdn)
            f1.write('\n')
db.commit()
db.close()
f0.close()
f1.close()