import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from matplotlib.dates import AutoDateFormatter, AutoDateLocator, DateFormatter
import sqlite3

#Connect to the database
conn = sqlite3.connect('weathertest.db')

#Set up date formatters for the x-axis
xtick_locator = AutoDateLocator()
xtick_formatter = AutoDateFormatter(xtick_locator)

#Set up the date parsing
dateparse = lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S')

#Get the date two days ago 
startdate = datetime.today() - timedelta(days=2)
startdate = startdate.strftime('%Y-%m-%d %H:%M:%S')

#Read the data
df = pd.read_sql("SELECT * from data where time > '" + startdate + "'", con = conn, parse_dates=['time'], index_col=['time'])

#Reset the index because of so many duplicate time stamps, otherwise pivot will not work.
df.reset_index(inplace=True)

#I had to reset the index in order to pivot because there were duplicate time stamps.
#Now in order to pivot, I have to do so on the new index and move 'time' to the columns.
#When it does this, 'time' gets separated for each channel (0, 1, 2, 3, C) so I have to 
#recombine all the time values into a single column again.  Doing this preserves the
#duplicate time stamps
df0 = df.pivot(columns='channel', values=['temperature_F','time', 'temperature_C'])
df0['time1'] = df0['time']['0']
df0['time2'] = df0['time1'].fillna(df0['time']['1'])
df0['time3'] = df0['time2'].fillna(df0['time']['2'])
df0['time4'] = df0['time3'].fillna(df0['time']['3'])
df0['time5'] = df0['time4'].fillna(df0['time']['C'])

#Get rid of the junk.
df0.drop(labels=['time1', 'time2', 'time3', 'time4'], inplace=True, axis=1)

#Convert C to F for channel 0 and C - the neighbors 
df0['X'] = df0['temperature_C']['0'] * (9/5) + 32
df0['Y'] = df0['temperature_C']['C'] * (9/5) + 32

#output data
df1 = pd.DataFrame()
df1['time'] = df0['time5']
df1['T0'] = df0['X']
df1['T1'] = df0['temperature_F']['1']
df1['T2'] = df0['temperature_F']['2']
df1['T3'] = df0['temperature_F']['3']
df1['TC'] = df0['Y']
df1 = df1[df1['time'].notnull()]
df1.to_csv('./serve/df1.csv', index=False)

#Start plotting stuff
plt.style.use('ggplot')
fig, ax = plt.subplots()
ax.scatter(df0['time5'], df0['X'], label='Neighbor1 ch0')
ax.scatter(df0['time5'], df0['temperature_F']['1'], label='Deck')
ax.scatter(df0['time5'], df0['temperature_F']['2'], label='Upstairs')
ax.scatter(df0['time5'], df0['temperature_F']['3'], label='Garage')
ax.scatter(df0['time5'], df0['Y'], label='Neighbor2 chC')
ax.xaxis.set_major_locator(xtick_locator)
ax.xaxis.set_major_formatter(xtick_formatter)
ax.set_ylim(df0['temperature_F']['1'].min()-10, df0['temperature_F']['1'].max()+10)
plt.xticks(rotation=90)
plt.legend(loc='upper left')
fig.tight_layout()
fig.savefig('./serve/weather_v2.png', fig_size=(7, 11))


