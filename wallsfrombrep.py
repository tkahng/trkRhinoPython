import trkRhinoPy as trp
import Rhino.Geometry as rg
import scriptcontext as sc
import rhinoscriptsyntax as rs
import Rhino


tol=sc.doc.ModelAbsoluteTolerance
trans=rg.CurveOffsetCornerStyle.Sharp

objs = rs.GetObjects('select polysrfs', rs.filter.polysurface, preselect=True)

def func(objid):
    obj = sc.doc.Objects.Find(objid).Geometry
    facecrvs = []
    curves = obj.DuplicateNakedEdgeCurves(1, 1)
    curves = rg.Curve.JoinCurves(curves, tol)
    curves = curves[0].Offset(rs.WorldXYPlane(),2,tol,trans)
    facecrvs.append(curves[0])
    brepfaces=[face.DuplicateFace(False) for face in obj.Faces]
    for x in brepfaces:
        crvs = x.DuplicateEdgeCurves()
        crvs = rg.Curve.JoinCurves(crvs, tol)
        crvs = crvs[0].Offset(rs.WorldXYPlane(),-1,tol,trans)
    #    pln = rs.CurvePlane(crvID)
        
        facecrvs.append(crvs[0])
    plnrsrf = rg.Brep.CreatePlanarBreps(facecrvs, tol)
    # solids = 
    rc = [sc.doc.Objects.AddBrep(c) for c in plnrsrf]
    return rc

map(func, objs)