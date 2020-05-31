import rhinoscriptsyntax as rs
import ghpythonlib.treehelpers as th
import scriptcontext as sc
import Rhino as rc
import System.Guid as Guid
import Grasshopper as gh

layers = rs.LayerNames()

def groupByPosition(pairs):
    newpairs = [[y for y in pairs if y[1]==x] for x in layers]
    return sorted(newpairs, key=lambda x:x[0][1])

crvpairs = [[x, rs.ObjectLayer(x)] for x in crvs]

b = th.list_to_tree(groupByPosition(crvpairs))

"""[summary]
"""