# import Rhino
# import Rhino.Geometry
# import Rhino.DocObjects
# from Rhino import *
# import Rhino
import Rhino
from Rhino import *

Rhino.Geometry
# import Rhino

# Rhino.Geometry.


# import Rhino
# import rhinoscriptsyntax as rs
# import scriptcontext as sc
# import trkRhinoPy as trp
# # import Rhino.Geometry


# objid = rs.GetObject("select polysrf", rs.filter.polysurface, preselect=True)

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