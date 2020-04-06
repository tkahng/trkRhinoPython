import csv
import rhinoscriptsyntax as rs

def CSVwrite():
    #Get the filename to create
    filter = "CSV File (*.csv)|*.csv|*.txt|All Files (*.*)|*.*||"
    filename = rs.SaveFileName("Save point coordinates as", filter)
    if( filename==None ): return

    dict = [
    {'Floor':'1', 'Use':'Retail', 'Square Footage':'6598', 'RoomID':'100'},
    {'Floor':'1', 'Use':'Retail', 'Square Footage':'1900', 'RoomID':'101'},
    {'Floor':'1', 'Use':'Retail', 'Square Footage':'1850', 'RoomID':'102'},
    {'Floor':'1', 'Use':'Restroom', 'Square Footage':'250', 'RoomID':'103'},
    {'Floor':'1', 'Use':'Maintenance', 'Square Footage':'150', 'RoomID':'104'}
    ]


    with open(filename, "wb") as csvfile:
        fieldnames = ('Floor', 'Use', 'Square Footage', 'Price', 'RoomID', 'Capacity')
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in dict:
            writer.writerow(row)

##########################################################################
# Check to see if this file is being executed as the "main" python
# script instead of being used as a module by some other python script
# This allows us to use the module which ever way we want.
if( __name__ == "__main__" ):
    CSVwrite()
