import trkRhinoPy as trp
import Rhino.Geometry as rg
import scriptcontext as sc
import rhinoscriptsyntax as rs
# import Rhino


tol=sc.doc.ModelAbsoluteTolerance
trans=rg.CurveOffsetCornerStyle.Sharp

objs = rs.GetObjects('select polysrfs', rs.filter.polysurface, preselect=True)
wallthickness = rs.GetReal('wall thickness', number=200)

def alignNormal(id):
    obj = sc.doc.Objects.Find(id)
    geo = obj.Geometry
    # print geo
#    srf = rs.coercesurface(id)
#    print srf
    srf = geo.Faces[0]
#    srf = face.UnderlyingSurface()
    # print srf
    normal = srf.NormalAt(srf.Domain(0).Mid, srf.Domain(1).Mid)
    # print normal
    # print normal.Z
    if normal.Z < 0:
        geo.Flip()
        sc.doc.Objects.Replace(id, geo)
        return id
#        return rs.FlipSurface(id, True)
    else:
        return id


def wallByBrep(objid, height, offout, offin):
    # height = float(rs.GetUserText(objid, 'height'))
    obj = sc.doc.Objects.Find(objid).Geometry
    facecrvs = []
    curves = obj.DuplicateNakedEdgeCurves(1, 1)
    curves = rg.Curve.JoinCurves(curves, tol)
    curves = curves[0].Offset(rs.WorldXYPlane(),offout,tol,trans)
    facecrvs.append(curves[0])
    brepfaces=[face.DuplicateFace(False) for face in obj.Faces]
    for x in brepfaces:
        crvs = x.DuplicateEdgeCurves()
        crvs = rg.Curve.JoinCurves(crvs, tol)
        crvs = crvs[0].Offset(rs.WorldXYPlane(),offin,tol,trans)
    #    pln = rs.CurvePlane(crvID)
        facecrvs.append(crvs[0])
    plnrsrf = rg.Brep.CreatePlanarBreps(facecrvs, tol)
    # rails = [rg.LineCurve(srf.Faces[0].PointAt(0,0), srf.Faces[0].PointAt(0,0) + rg.Point3d(0,0,height)) for srf in plnrsrf]
    solids = [rg.BrepFace.CreateExtrusion(srf.Faces[0], rg.LineCurve(srf.Faces[0].PointAt(0,0), srf.Faces[0].PointAt(0,0) + rg.Point3d(0,0,height)), True) for srf in plnrsrf]
    solidsrc = [sc.doc.Objects.AddBrep(c) for c in solids]
    # railsrc = [sc.doc.Objects.AddCurve(c) for c in rails]
    # facecrvsrc = [sc.doc.Objects.AddCurve(c) for c in facecrvs]
    # rc = [sc.doc.Objects.AddBrep(c) for c in plnrsrf]
    return solidsrc

def func(obj):
    obj = alignNormal(obj)
    width = wallthickness/2
    height = float(rs.GetUserText(obj, "height"))
    # lvl = rs.GetUserText(obj, 'level')    
    walls = wallByBrep(obj, height, width, -width)
    [trp.copySourceData(wall, obj) for wall in walls]

map(func, objs)