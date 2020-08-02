import trkRhinoPy as trp
import rhinoscriptsyntax as rs
from rhinopythonscripts.GeomTools import getSelected
import scriptcontext as sc
from rhinopythonscripts import Smart
import Rhino

# objs = rs.GetObjects()
targId = rs.GetObject("Select the first object to replace")
#if not targId:return

rhobj = sc.doc.Objects.Find(targId)
#geo = obj.Geometry


rhobjlist = getSelected()

sf = Smart.RhinoObjectsToSmartFeatures(rhobjlist)

print sf[0].attributes

# import Rhino.Geometry
# import Grasshopper as gh

# gh.tree

# import 
# rs.GetObject()
