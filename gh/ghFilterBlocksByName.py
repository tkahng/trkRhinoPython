import rhinoscriptsyntax as rs
import ghpythonlib.treehelpers as th
import scriptcontext as sc
import Rhino as rc

sc.doc = rc.RhinoDoc.ActiveDoc

name = rs.BlockInstanceName(x)

a = True if name == y else False