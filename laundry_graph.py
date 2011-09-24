from BeautifulSoup import BeautifulSoup
import urllib2


def getRoomInfo(id):
    doc = urllib2.urlopen("http://case-asi.esuds.net/RoomStatus/machineStatus.i?bottomLocationId={0}".format(id) ,"").read()
    # TODO: Error checking

    soup = BeautifulSoup(doc)
    table = [
        [column.contents for column in row.findAll("td")] #Unpack each row
        for row
        in soup.table.findAll("tr")
    ]
    table = filter(lambda row: len(row) == 5, table) #Remove all rows which don't describe machines (data rows have five columns)
    table = [
        (
            int(row[1][0]) ,
            row[2][0] ,
            row[3][1].contents[0]
        )
        for row
        in table
    ]
    return table
