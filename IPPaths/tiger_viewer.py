#!/usr/bin/python

import tiger_log as log
import subprocess
import sqlite3
import argparse
import datetime
import cv, cv2
import sys
import re

# parse the date input
#parser = argparse.ArgumentParser()
#parser.add_argument("date", help="input a date to search for video files")
#args = parser.parse_args()

def process_date(date):
   try:
        date = datetime.datetime.strptime(date,"%Y/%m/%d/%H")
        return True
    except ValueError:
        return False


# Prompt for date
date = raw_input("\nPlease enter a date-time to be searched (yyyy/mm/dd/hh): ")
while (True):
   processed = process_date(date)
   if (processed):
       print 'Searching date-time: ', date
       break
   else:
       date = raw_input("\nError processing date-time. Please re-enter date-time to be searched (yyyy/mm/dd/hh): ")       


# Get appropriate videos from tigerlog.db // Add paths to file: ex. vid_list.txt
db = None
try:
    print '\nOpening database to retrieve paths'
    tiger_db, cursor = log.open_data_base()     # in tiger_log.py
    print 'Database opened successfully'

    print '\nSelecting files from date-time: ', date    
    dated = log.select_date(date)
    print dated


    print '\nClosing database'
    log.close_data_base(tiger_db)
    print 'Database closed successfully'

    # Write date paths to vid_paths.txt
    for path in dated:
        with open(vid_paths.txt, 'w') as output:
            output.write('file '+ path + '\n')    

except sqlite3.Error, e:
    print "Error %s:" % e.args[0]
    sys.exit(1)


# Stitch toegether positve frames using ffmpeg
print '\nRunning compile_list.sh'
subprocess.call("./compile_list.sh", shell=True)
print 'Sucessful.'


# Return stitched videos and play in viewer
cap = cv2.VidCapture(vid_path)
while cap.isOpened():
    ret, frame = cap.read()
    cv2.imshow('tiger_vid',frame)
cap.release()
cv2.destroyAllWindows()
