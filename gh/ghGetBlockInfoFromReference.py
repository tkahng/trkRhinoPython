# input is guid of referenced block

import rhinoscriptsyntax as rs
import ghpythonlib.treehelpers as th
import scriptcontext as sc
import Rhino as rc

sc.doc = rc.RhinoDoc.ActiveDoc

a = rs.BlockInstanceName(x)
b = rs.BlockInstanceXform(x)