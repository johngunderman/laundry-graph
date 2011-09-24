from BeautifulSoup import BeautifulSoup
import urllib2

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
