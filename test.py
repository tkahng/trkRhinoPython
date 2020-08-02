import trkRhinoPy as trp
import rhinoscriptsyntax as rs
from rhinopythonscripts.GeomTools import getSelected
import scriptcontext as sc
from rhinopythonscripts import Smart
import Rhino

# objs = rs.GetObjects()
targIds = rs.GetObjects("Select the first object to replace")
#if not targId:return

obj = [sc.doc.Objects.Find(x) for x in targIds]
#geo = obj.Geometry


#rhobjlist = getSelected()

sf = Smart.RhinoObjectsToSmartFeatures(obj)

print [x.attributes for x in sf]

# import Rhino.Geometry
# import Grasshopper as gh

# gh.tree

# import 
# rs.GetObject()
