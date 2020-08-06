import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino

"""Offsets planar curves both sides curves in their curve plane and adds ends
If curve plane can't be determined(lines for example), uses active CPlane
Script by Mitch Heynick 23.05.15""" 

def OffsetCurve2Sides (crvID, dist, t_style, conn, tol):
    if rs.IsLine(crvID): plane = rs.ViewCPlane()
    else: plane = rs.CurvePlane(crvID)
    crv=sc.doc.Objects.Find(crvID).Geometry
    
    if t_style==1: trans=Rhino.Geometry.CurveOffsetCornerStyle.Sharp
    elif t_style==2: trans=Rhino.Geometry.CurveOffsetCornerStyle.Round
    elif t_style==3: trans=Rhino.Geometry.CurveOffsetCornerStyle.Smooth
    elif t_style==4: trans=Rhino.Geometry.CurveOffsetCornerStyle.Chamfer
    offset1=crv.Offset(plane,dist,tol,trans)
    if offset1:
        offset2=crv.Offset(plane,-dist,tol,trans)
        if offset2:
            if len(offset1)== 1 and len(offset2)==1:
                offset1ID=sc.doc.Objects.AddCurve(offset1[0])
                offset2ID=sc.doc.Objects.AddCurve(offset2[0])
                if conn >= 0 and not rs.IsCurveClosed(crvID):
                    AddEndsToOffset(offset1ID, offset2ID, conn, dist)
                #don't care if ends get made or not, exit afterward
                return True

def CrvSegmentMidPt(crv, n):
    if rs.IsPolyline(crv):
        verts = rs.PolylineVertices(crv)
        midPt = (verts[n] + verts[n+1])/2
    elif rs.IsPolyCurve(crv):
        midPt = rs.CurveMidPoint(crv, n)
    else:
        midPt = rs.CurveMidPoint(crv)
    return midPt
    
def AddEndsToOffset(offset0,offset1,conn,dist):
    OC1SP = rs.CurveStartPoint(offset0)
    OC2SP = rs.CurveStartPoint(offset1)
    OC1EP = rs.CurveEndPoint(offset0)
    OC2EP = rs.CurveEndPoint(offset1)
    line0=Rhino.Geometry.Line(OC1SP,OC2SP)
    line1=Rhino.Geometry.Line(OC1EP,OC2EP)
    
    result=[offset0,offset1] 
    if conn == 0:    
        result.append(sc.doc.Objects.AddLine(line0))
        result.append(sc.doc.Objects.AddLine(line1))
    else:
        #add arc from crv end pts and tan direction - save arcs for next section
        dom=rs.CurveDomain(offset0)
        t_vec=rs.CurveTangent(offset0,dom[0])
        t_vec.Reverse()
        arc0=Rhino.Geometry.Arc(OC1SP,t_vec,OC2SP)
        t_vec=rs.CurveTangent(offset0,dom[1])
        arc1=Rhino.Geometry.Arc(OC1EP,t_vec,OC2EP)
        
        if conn==1:
            result.append(sc.doc.Objects.AddArc(arc0))
            result.append(sc.doc.Objects.AddArc(arc1))
        else:
            #translate lines to arc midpoints, then extend offset curves to ends
            xform=rs.XformTranslation(arc0.MidPoint-((line0.From+line0.To)/2))
            line0.Transform(xform)
            xform=rs.XformTranslation(arc1.MidPoint-((line1.From+line1.To)/2))
            line1.Transform(xform)
            result.append(sc.doc.Objects.AddLine(line0))
            result.append(sc.doc.Objects.AddLine(line1))
            rs.ExtendCurvePoint(offset0, 0, line0.From)
            rs.ExtendCurvePoint(offset1, 0, line0.To)
            rs.ExtendCurvePoint(offset0, 1, line1.From)
            rs.ExtendCurvePoint(offset1, 1, line1.To)
    
    if len(result)>2: rs.JoinCurves(result, True)

def plcrv_filt(rhino_object, geometry, component_index):
    return rs.IsCurvePlanar(geometry)

def OffsetMulticrvs2SidesWEnds():
    #user input section
    msg="Select planar curve(s) to offset both sides"
    crvs = rs.GetObjects(msg,4,preselect=True,custom_filter=plcrv_filt)
    if not crvs: return
        
    tol = sc.doc.ModelAbsoluteTolerance
    t_choice = ["Sharp", "Round", "Smooth", "Chamfer"] 
    e_choice = ["None", "Straight", "Arc", "OffsetStraight"]
    
    #Get previous settings
    if "OffsetCrvs_Dist" in sc.sticky: old_dist = sc.sticky["OffsetCrvs_Dist"]
    else: old_dist = 1.0
    if "OffsetCrvs_TChoice" in sc.sticky: old_trans = sc.sticky["OffsetCrvs_TChoice"]
    else: old_trans = "Sharp"
    if "OffsetCrvs_EChoice" in sc.sticky: old_ends = sc.sticky["OffsetCrvs_EChoice"]
    else: old_ends = "None"
    
    off_dist = rs.GetReal("Distance to offset", old_dist, tol)
    if not off_dist: return
    
    trans_type = rs.GetString("Offset transition?", old_trans, t_choice)
    if not trans_type: return
    if trans_type=="Sharp": tt = 1
    elif trans_type=="Round": tt = 2
    elif trans_type=="Smooth": tt = 3
    elif trans_type=="Chamfer": tt = 4
    else: return
        
    end_type = rs.GetString("End connection type?", old_ends, e_choice)
    if not end_type: return
    if end_type=="None" : conn = -1
    elif end_type=="Straight" : conn = 0
    elif end_type=="Arc" : conn = 1
    elif end_type=="OffsetStraight" : conn = 2
    else: return
    
    rs.EnableRedraw(False)
    rs.UnselectAllObjects
    
    count = 0
    for crv in crvs:     
        success = OffsetCurve2Sides(crv, off_dist, tt, conn, tol)        
        if success: count+=1       
    
    if count<len(crvs):
        err_msg=" Unable to offset {} curves".format(len(crvs)-count)
    else: err_msg=""
    print "Successfully offset {} curves.".format(count)+err_msg
    
    #Set preferences
    sc.sticky["OffsetCrvs_Dist"] = off_dist
    sc.sticky["OffsetCrvs_TChoice"] = trans_type
    sc.sticky["OffsetCrvs_EChoice"] = end_type
OffsetMulticrvs2SidesWEnds()