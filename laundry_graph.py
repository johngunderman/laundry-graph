from BeautifulSoup import BeautifulSoup
import urllib2
import sqlite3
import os

# SCHEMA:
# date machine# type status roomID

# These numbers are assigned to each building by eSuds.
# We chose a sample of buildings on the campus.
roomnames = {
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

DB_NAME = './laundry.db'


# if our db doesn't exist, make sure to set up the schema.
def initializeDB():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
"""
CREATE TABLE IF NOT EXISTS datapoints (id INTEGER PRIMARY KEY ASC,
date INTEGER, machine_num INTEGER,
type TEXT, status INTEGER, building_id INTEGER);
"""
        )
    conn.commit()
    conn.close()

def insertRecord(machine_num, type, status, room_id):
    """
    insert a data point into our database for the given values.

    Arguments:
    - `machine_num`: The number of the given washer/dryer (generally 1-4)
    - `type`: whether or not this machine is a washer or dryer
    - `status`: what state our washer/dryer is in. Values include:
               1 - In Use
               2 - Available
               3 - Unavailable
               4 - Cycle Complete
    - `building_id`: The number corresponding to the given building.
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        """
INSERT INTO datapoints (id, date, machine_num, type, status, room_id)
VALUES (NULL,DATETIME('NOW'),?,?,?,?)
"""
        , (machine_num, type, status, room_id)
        )
    conn.commit()
    conn.close()



def getRoomInfo(id):
    doc = urllib2.urlopen("http://case-asi.esuds.net/RoomStatus/machineStatus.i?bottomLocationId={0}".format(id) ,"").read()
    # TODO: Error checking

    soup = BeautifulSoup(doc)
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
