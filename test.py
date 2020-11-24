# import Rhino
# import Rhino.Geometry
# import Rhino.DocObjects
# from Rhino import *
# import Rhino
import Rhino
#from Rhino import *

#Rhino.Geometry
# import Rhino

# Rhino.Geometry.


# import Rhino
import rhinoscriptsyntax as rs
import scriptcontext as sc
# import trkRhinoPy as trp
# # import Rhino.Geometry

ids = rs.GetObjects("select polysrf", rs.filter.polysurface|rs.filter.surface, preselect=True)

rs.EnableRedraw(False)

breps = [rs.coercegeometry(id) for id in ids]

sils = []

for brep in breps:
    edges = brep.Edges
    edgecrvs = [e.DuplicateCurve() for e in edges]
    sils.extend(edgecrvs)
print sils

silscrv = [sc.doc.Objects.AddCurve(sil) for sil in sils]
rs.UnselectAllObjects()
rs.SelectObjects(silscrv)
rs.Command('_CurveBoolean AllRegions _Enter')
rs.DeleteObjects(silscrv)


#flats = [rg.Curve.ProjectToPlane(e, rs.WorldXYPlane()) for e in edgecrvs]
#print flats
#a = flats
#
#crvunion = rg.Curve.CreateBooleanUnion(flats, Rhino.RhinoDoc.ActiveDoc.ModelAbsoluteTolerance)
#print list(crvunion)

# brep = rs.coercebrep(objid)

# # edges = brep.Edges

# # a =  brep.Edges[0].Valence
# # Rhino.Geometry.BrepEdge.Valence.__repr__()
# # print a.__repr__()

# # print dir(brep.Edges[0])

# for edge in brep.Edges:
#     # print edge.Valence  
#     if edge.Valence == Rhino.Geometry.EdgeAdjacency.Interior:
#         print edge
#         sc.doc.Objects.AddCurve(edge.EdgeCurve)