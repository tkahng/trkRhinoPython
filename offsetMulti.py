import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino
import trkRhinoPy as trp

tol = sc.doc.ModelAbsoluteTolerance
trans=Rhino.Geometry.CurveOffsetCornerStyle.Sharp

crvs = rs.GetObjects("select crvs", rs.filter.curve, preselect=True)
dist = rs.GetReal("dist")

def Func(crvID):


    if rs.IsLine(crvID): plane = rs.ViewCPlane()
    else: plane = rs.CurvePlane(crvID)
    crv=sc.doc.Objects.Find(crvID).Geometry
    
    # if t_style==1: trans=Rhino.Geometry.CurveOffsetCornerStyle.Sharp
    # elif t_style==2: trans=Rhino.Geometry.CurveOffsetCornerStyle.Round
    # elif t_style==3: trans=Rhino.Geometry.CurveOffsetCornerStyle.Smooth
    # elif t_style==4: trans=Rhino.Geometry.CurveOffsetCornerStyle.Chamfer
    offset1=crv.Offset(plane,dist,tol,trans)
    offset1ID=sc.doc.Objects.AddCurve(offset1[0])
    # if offset1:
    #     offset2=crv.Offset(plane,-dist,tol,trans)
    #     if offset2:
    #         if len(offset1)== 1 and len(offset2)==1:
    #             offset1ID=sc.doc.Objects.AddCurve(offset1[0])
    #             offset2ID=sc.doc.Objects.AddCurve(offset2[0])
    #             if conn >= 0 and not rs.IsCurveClosed(crvID):
    #                 AddEndsToOffset(offset1ID, offset2ID, conn, dist)
    #             #don't care if ends get made or not, exit afterward
    #             return True






offsetcrvs = map(Func, crvs)
# rs.UnselectObjects(crvs)
# rs.SelectObjects(offsetcrvs)