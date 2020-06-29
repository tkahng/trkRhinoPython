# input is guid of referenced block

import rhinoscriptsyntax as rs
import ghpythonlib.treehelpers as th
import scriptcontext as sc
import Rhino as rc

sc.doc = rc.RhinoDoc.ActiveDoc

cameraPos = rs.ViewCamera()

cameraPos.Z = 0

xform = rs.BlockInstanceXform(x)
plane = rs.PlaneTransform(rs.WorldXYPlane(), xform)

viewdir = cameraPos - plane.Origin
#viewdir = plane.Origin - cameraPos


#angle = rs.VectorAngle(plane.YAxis, viewdir)
angle = rs.VectorAngle(viewdir, plane.YAxis)

newplane = rs.RotatePlane(plane, angle, plane.ZAxis)

a = xform

b = plane

c = cameraPos

d = viewdir

e = plane.YAxis

f = newplane

