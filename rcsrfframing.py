import Rhino
import rhinoscriptsyntax as rs

#Get a reference to the document
doc = Rhino.RhinoDoc.ActiveDoc
#Get all the objects in the document
#objects = doc.Objects
#Get all the selected objects
selectedObjects = [o for o in doc.Objects.GetSelectedObjects(False,False)]
#try to get the first selected item, if it fails print a message to the command line
print selectedObjects