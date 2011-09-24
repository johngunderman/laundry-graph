#!/usr/bin/python2.7
from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen, URLError
import sqlite3
import os
import time

POLL_INTERVAL = 2 #in seconds
DB_NAME = './laundry.db'
ESUDS_URL = "http://case-asi.esuds.net/RoomStatus/machineStatus.i?bottomLocationId={0}"

# These numbers are assigned to each building by eSuds.
# We chose a sample of buildings on the campus.
rooms = {
    1398: "Clarke Tower",
    1403: "Hitchcock",
    1407: "Pierce",
    1415: "Raymond",
    1427: "Staley",
    1431: "Howe",
    1443: "Village, House 1",
    1448: "Village, House 6",
    4193: "Glaser",

}

# SCHEMA:
# date machine# type status roomID

# if our db doesn't exist, make sure to set up the schema.
def initializeDB():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
"""
CREATE TABLE IF NOT EXISTS datapoints (id INTEGER PRIMARY KEY,
date INTEGER, machine_num INTEGER,
type TEXT, status INTEGER, room_id INTEGER);
"""
        )
    conn.commit()
    conn.close()


def getRoomInfo(id):
    page = urlopen(ESUDS_URL.format(id) ,"")
    
    soup = BeautifulSoup(page.read())
    table = [ #Unpack the table
        [column.contents for column in row.findAll("td")] #Unpack each row.  Some rows have <th> elements.  We filter those out below.
        for row
        in soup.table.findAll("tr")
    ]

    table = filter(lambda row: len(row) == 5, table) #Remove all rows which aren't data rows (data rows have five columns)

    table = [
        (
            int(row[1][0]) , #Machine ID
            row[2][0] , #Machine type
            row[3][1].contents[0] #Status
        )
        for row
        in table
    ]
    return table

def data_loop():
    data = {}
    succeeded = 0
    errors = []
    for i in rooms:
        try:
            data[i] = getRoomInfo(i)
            #TODO: Add to db
            succeeded += 1
        except URLError as e:
            errors.append(e)
    print("{0} requests succeeded, {1} errors".format(succeeded, len(errors)))
    if len(errors) > 0:
	for e in errors:
            print("\t{0}".format(e))
	print

def main():
    try:
        while(True):
            start = time.time()
            data_loop()
            time.sleep(POLL_INTERVAL - (time.time() - start)) # Sleep POLL_INTERVAL seconds, but subtract the time taken querying the server
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
