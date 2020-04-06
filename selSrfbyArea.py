import Rhino
#Get a reference to the document
doc = Rhino.RhinoDoc.ActiveDoc
#Get all the objects in the document
objects = doc.Objects
#Get all the selected objects
selectedObjects = [o for o in doc.Objects.GetSelectedObjects(False,False)]
#try to get the first selected item, if it fails print a message to the command line
try:
    firstSelected = selectedObjects[0]
    objects.UnselectAll()
except:
    print "Select an object and re-run command"

#get the area of the first selected item
try:
    targetArea = Rhino.Geometry.AreaMassProperties.Compute(firstSelected.Geometry).Area
except:
    "Unable to measure object area"

#set up a list to hold all the items we want to select
toSelect = []
#for every item in the rhino document, try to get its area and compare it to the target area
for rhObj in objects:
    try:
        area = Rhino.Geometry.AreaMassProperties.Compute(rhObj.Geometry).Area
        if abs(targetArea - area ) < 0.01:
            toSelect.append(rhObj)
    except:
        pass
#for each item in the "to select" list, select it
for item in toSelect:
    objects.Select(item.Id)