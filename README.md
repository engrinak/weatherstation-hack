# weatherstation-hack
Temperature plot / display for cheap home weather station using SDR, python and javascript.

# weather1.csv
This is the output from rtl_433 in csv format, the raw data logged by the SDR.

# rtl_csv_to_sql2.py
This is the script that appends csv data into the weathertest.db database, via SQLite.  A csv file is passed to the script as a command line argument.  Call the script like this: `python rtl_csv_to_sql2.py weather1.csv`

# plotweather_v2.py
This script loads data from weathertest.db, pivots and exports a png plot and csv data (df1.csv) into the serve folder.  

# serve
This is the folder that is served via HTTP on the local network.  It contains the index, df1.csv, and javascript.
