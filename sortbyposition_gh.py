import rhinoscriptsyntax as rs
import ghpythonlib.treehelpers as th
import scriptcontext as sc
import Rhino as rc
import System.Guid as Guid
# import Grasshopper as gh

# sc.doc = rc.RhinoDoc.ActiveDoc
# # rc.RhinoDoc.Objects.
doc = Rhino.RhinoDoc.ActiveDoc
# rc.RhinoDoc.SelectObjects
# rs.object
print(rs.coercerhinoobject(guids[0]))
print(type(srfs[0]))
print(srfs[0])
print(rs.coerceguid(srfs[0]))

seq = [x * dist + dist for x in range(count)]
intervals = [(x - dist, x) for x in seq]

def groupByPosition(pairs):
    # values = set(map(lambda x:x[1], pairs))
    newpairs = [[y for y in pairs if min(x) < y[1] < max(x)] for x in intervals]
    # print newpairs
    return sorted(newpairs, key=lambda x:x[0][1])

srfpairs = [[x, rs.SurfaceAreaCentroid(x)[0][axis], str(x)] for x in srfs]
guidout = [rs.coercerhinoobject(x) for x in guids]
print(srfpairs[0][0])

# grouped = groupByPosition(srfpairs)

# Intervals = th.list_to_tree(intervals)

b = th.list_to_tree(groupByPosition(srfpairs))

a = srfs
# b = guidout
"""[summary]
"""


# import rhinoscriptsyntax as rs
# import System.Guid as Guid

# import Rhino


# doc = Rhino.RhinoDoc.ActiveDoc

# gid = Guid.Parse(x)

# obj = doc.Objects.Find(gid)
# geo = rs.coercegeometry(gid)
# layer = doc.Layers[obj.Attributes.LayerIndex].Name
# a = doc.Layers[obj.Attributes.LayerIndex].Name
# b = geo

# from ghpythonlib.componentbase import executingcomponent as component
# import Grasshopper, GhPython
# import System
# import Rhino
# import rhinoscriptsyntax as rs

# class MyComponent(component):
    
#     def RunScript(self, srfs, dist, count, axis):
#         import rhinoscriptsyntax as rs
#         import ghpythonlib.treehelpers as th
        
#         seq = [x * dist + dist for x in range(count)]
#         intervals = [(x - dist, x) for x in seq]
        
#         def groupByPosition(pairs):
#             # values = set(map(lambda x:x[1], pairs))
#             newpairs = [[y for y in pairs if min(x) < y[1] < max(x)] for x in intervals]
#             # print newpairs
#             return sorted(newpairs, key=lambda x:x[0][1])
        
#         srfpairs = [[x, rs.SurfaceAreaCentroid(x)[0][axis]] for x in srfs]
        
#         # grouped = groupByPosition(srfpairs)
        
#         # Intervals = th.list_to_tree(intervals)
        
#         b = th.list_to_tree(groupByPosition(srfpairs))
        
#         # return outputs if you have them; here I try it for you:
#         return b
