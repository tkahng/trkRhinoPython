import trkRhinoPy as trp
import rhinoscriptsyntax as rs
from rhinopythonscripts.GeomTools import getSelected
import scriptcontext as sc
from rhinopythonscripts import Smart
import Rhino as rc
import json
import ast


sc.doc = rc.RhinoDoc.ActiveDoc

src = sc.sticky["levels"]

lvldict = ast.literal_eval(src)

#lvlel = map(lambda x: zip(x['level'], x['elevation']), lvldict)

lvlk = [x['level'] for x in lvldict]
lvlk = [x['lelevation'] for x in lvldict]

print lvlk, lvll



#print lvlel
print type(lvlel)

## objs = rs.GetObjects()
#targId = rs.GetObject("Select the first object to replace")
##if not targId:return
#
#rhobj = sc.doc.Objects.Find(targId)
##geo = obj.Geometry
#
#
#rhobjlist = getSelected()
#
#sf = Smart.RhinoObjectsToSmartFeatures(rhobjlist)
#
#print sf[0].attributes
#
## import Rhino.Geometry
## import Grasshopper as gh
#
## gh.tree
#
## import 
## rs.GetObject()
