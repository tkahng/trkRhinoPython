"""Provides a scripting component.
    Inputs:
        x: The x script variable
        y: The y script variable
    Output:
        a: The a output variable"""

__author__ = "인시공현장PC"
__version__ = "2020.08.06"

import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino

# import Rhino.Geometry as rg
# import Rhino.Geometry
# from Rhino.Geometry import Brep

sc.doc = Rhino.RhinoDoc.ActiveDoc

# rg.Curve.Offset()

print x

tol=sc.doc.ModelAbsoluteTolerance
dist = -2
crvID = x
brepid = y


plane = rs.CurvePlane(crvID)
#plane = rs.WorldXYPlane()

crv=sc.doc.Objects.Find(crvID).Geometry

trans=Rhino.Geometry.CurveOffsetCornerStyle.Sharp

offset1=crv.Offset(plane,dist,tol,trans)

polysrf = sc.doc.Objects.Find(brepid).Geometry
print polysrf
curves = polysrf.DuplicateNakedEdgeCurves(1, 1)
tolerance = sc.doc.ModelAbsoluteTolerance * 2.1
curves = Rhino.Geometry.Curve.JoinCurves(curves, tolerance)
curves = curves[0].Offset(rs.WorldXYPlane(),2,tol,trans)
#curves = curves[0]
#facecrvs.append(curves)
#faces = polysrf.Faces

a = offset1
b = curves

brepfaces=[face.DuplicateFace(False) for face in polysrf.Faces]

facecrvs = []
facecrvs.append(curves[0])
for x in brepfaces:
    crvs = x.DuplicateEdgeCurves()
    crvs = Rhino.Geometry.Curve.JoinCurves(crvs, tolerance)
    crvs = crvs[0].Offset(rs.WorldXYPlane(),-1,tol,trans)
#    pln = rs.CurvePlane(crvID)
    
    facecrvs.append(crvs[0])


#c = facecrvs
print brepfaces
print curves[0]
#border = rs.DuplicateSurfaceBorder(y)
print len(b)
#print faces
print facecrvs
#b = border
#a = plane
c = facecrvs

plnrsrf = Rhino.Geometry.Brep.CreatePlanarBreps(facecrvs, tolerance)
d = plnrsrf
print plnrsrf
#rc = [sc.doc.Objects.AddCurve(c) for c in facecrvs]