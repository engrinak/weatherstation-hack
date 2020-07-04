import pandas as pd
import sqlite3
from datetime import datetime
import sys

mydb = 'weathertest.db'
csvfile = sys.argv[1] 

def dateparse(x):
    return datetime.strptime(x, '%Y-%m-%d %H:%M:%S')

def undateparse(x):
    return datetime.strftime(x, '%Y-%m-%d %H:%M:%S') 

df = pd.read_csv(csvfile, low_memory= False, header=0, index_col=0)
#make a string with the correct number of question marks
insQmrks = '?,' * (len(df.columns) + 1)
insQmrks = insQmrks[0:len(insQmrks)-1]

def pd_sqlt(df, mydb, idxcol, insQmrks):
    conn = sqlite3.connect(mydb)
    c = conn.cursor()
    DateTimes = []

    try: #create table if it doesn't exist
        df.to_sql(name='data', con=conn, if_exists='fail')
    except:
        pass
    
    #Count the columns in the dataframe
    for row in c.execute('SELECT ' + idxcol + ' FROM data'):
        DateTimes.append(row[0])

    #filter out 'time' and null from DateTimes
    DateTimes = [x for x in DateTimes if x != 'time']
    DateTimes = [x for x in DateTimes if x != '']

    df = df[df.index != 'time']
    df = df[df.index.notnull()]
    df.index = df.index.map(dateparse)
    df = df[df.index > datetime.strptime(DateTimes[-1], '%Y-%m-%d %H:%M:%S')]
   
    #Convert index back to string
    df.index = df.index.map(undateparse)
    
    #Write data back into database
    for row in df.itertuples(name=None):
        c.execute('INSERT INTO data VALUES(' + insQmrks + ')', row)
    

    conn.commit()
    conn.close()




pd_sqlt(df, mydb, 'time', insQmrks)



