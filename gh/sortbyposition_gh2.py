import rhinoscriptsyntax as rs
import ghpythonlib.treehelpers as th
import scriptcontext as sc
# import Rhino


print(type(srfs[0]))
print(srfs[0])

seq = [x * dist + dist for x in range(count)]
intervals = [(x - dist, x) for x in seq]

def groupByPosition(pairs):
    # values = set(map(lambda x:x[1], pairs))
    newpairs = [[y for y in pairs if min(x) < y[1] < max(x)] for x in intervals]
    # print newpairs
    return sorted(newpairs, key=lambda x:x[0][1])

srfpairs = [[x, rs.SurfaceAreaCentroid(x)[0][axis], str(x)] for x in srfs]

print(srfpairs[0])

# grouped = groupByPosition(srfpairs)

# Intervals = th.list_to_tree(intervals)

b = th.list_to_tree(groupByPosition(srfpairs))

a = srfs
"""[summary]
"""

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
