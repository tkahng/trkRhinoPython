"""Unrolls a series of surfaces/polysurfaces, with possibility to number.
Options: Keep object layer/color; Explode yes/no; Number yes/no; X extents limit
so that obects are not unrolled all in one line - 0=no extents set.
Script by Mitch Heynick, version 02.11.15 Re-written with RhinoCommon Unroller"""

import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino
    
def AddDotToObjCtr(objIDs,text,transfer=True):
    #adds a dot to object(s) bounding box center and groups dot with object(s)
    bb = rs.BoundingBox(objIDs)
    if bb:
        dotID=rs.AddTextDot(text,(bb[0]+bb[6])/2)
        if transfer: TransferColorLayer(dotID,objIDs[0])
        objIDs.append(dotID)
        group = rs.AddGroup()
        test=rs.AddObjectsToGroup(objIDs, group)
        return dotID
        
def TransferColorLayer(target_IDs,source_ID):
    rs.ObjectLayer(target_IDs,rs.ObjectLayer(source_ID))
    rs.ObjectColor(target_IDs,rs.ObjectColor(source_ID))

def CommandLineOptions(prompt,msg,ini,limits):
    gp = Rhino.Input.Custom.GetPoint()
    gp.SetCommandPrompt(prompt)

    blnOption0 = Rhino.Input.Custom.OptionToggle(ini[0],limits[0][0],limits[0][1])
    blnOption1 = Rhino.Input.Custom.OptionToggle(ini[1],limits[1][0],limits[1][1])
    blnOption2 = Rhino.Input.Custom.OptionToggle(ini[2],limits[2][0],limits[2][1])
    dblOption3 = Rhino.Input.Custom.OptionDouble(ini[3],limits[3][0],limits[3][1])
    dblOption4 = Rhino.Input.Custom.OptionDouble(ini[4],limits[4][0],limits[4][1])
    
    gp.AddOptionToggle(msg[0],blnOption0)
    gp.AddOptionToggle(msg[1],blnOption1)
    gp.AddOptionToggle(msg[2],blnOption2)
    gp.AddOptionDouble(msg[3],dblOption3)
    gp.AddOptionDouble(msg[4],dblOption4)
    gp.AcceptNothing(True)
    point=Rhino.Geometry.Point3d(0,0,0)
    
    while True:
        get_rc = gp.Get()
        a=blnOption0.CurrentValue
        b=blnOption1.CurrentValue
        c=blnOption2.CurrentValue
        d=dblOption3.CurrentValue
        e=dblOption4.CurrentValue
        if gp.CommandResult()== Rhino.Commands.Result.Cancel:
            return
        elif gp.CommandResult()== Rhino.Commands.Result.Nothing:
            break
        elif get_rc==Rhino.Input.GetResult.Point:
            point = gp.Point()
            break
        elif get_rc==Rhino.Input.GetResult.Option:
            continue
        break
    return (a,b,c,d,e,point)

def MultiUnroll():
    
    msg="Select surface/polysurface objects to unroll"
    brepIDs = rs.GetObjects(msg,8+16,preselect=True)
    if not brepIDs: return
    
    msg="Select curves and/or points to unroll with surfaces, or Enter to continue"
    otherIDs=rs.GetObjects(msg,1+4+8192)
    
    if "MultiUR_Numbering" in sc.sticky: user_num = sc.sticky["MultiUR_Numbering"]
    else: user_num=True
    
    if "MultiUR_Explode" in sc.sticky: user_exp = sc.sticky["MultiUR_Explode"]
    else: user_exp=False
    
    if "MultiUR_Properties" in sc.sticky: user_prop = sc.sticky["MultiUR_Properties"]
    else: user_prop=False
    
    if "MultiUR_Spacing" in sc.sticky: user_space = sc.sticky["MultiUR_Spacing"]
    else: user_space=1.0
    
    if "MultiUR_XLimit" in sc.sticky: user_xl = sc.sticky["MultiUR_XLimit"]
    else: user_xl=0
    
    prompt="Start point for unrolls - press Enter for world 0"
    msg=["NumberObjects","Explode","KeepProperties","LayoutSpacing","XExtents"]
    ini=[user_num,user_exp,user_prop,user_space,user_xl]
    limits=[["No","Yes"],["No","Yes"],["No","Yes"],[True,0],[True,0]]
    result=CommandLineOptions(prompt,msg,ini,limits)
    if not result: return
    x_extents=result[4]
    new_sp=result[5]
    
    #initialize
    max_y=new_sp.Y
    x_origin=new_sp.X
    exceed_warning=False
    ur_number=0 ; no_unroll=0 ; crvs=[] ; pts=[] ; dots=[]
    tol=sc.doc.ModelAbsoluteTolerance
    #get underlying geometry objects
    objs=[sc.doc.Objects.Find(objID).Geometry for objID in brepIDs]
    if otherIDs:
        for objID in otherIDs:
            if rs.IsCurve(objID):
                crvs.append(sc.doc.Objects.Find(objID).Geometry)
            elif rs.IsPoint(objID):
                pts.append(sc.doc.Objects.Find(objID).Geometry)
            else:
                dots.append(sc.doc.Objects.Find(objID).Geometry)
                
    #run the unroller
    rs.EnableRedraw(False)
    for i,obj in enumerate(objs):
        if isinstance(obj,Rhino.Geometry.Extrusion): obj=obj.ToBrep()
        ur=Rhino.Geometry.Unroller(obj)
        if result[1]: ur.ExplodeOutput=True
        if len(crvs)>0:
            for crv in crvs: ur.AddFollowingGeometry(crv)
        if len(pts)>0:
            for pt in pts: ur.AddFollowingGeometry(pt)
        if len(dots)>0:
            for dot in dots: ur.AddFollowingGeometry(dot)
        unroll=ur.PerformUnroll()
        if unroll[0]:
            #something was unrolled
            ur_number+=1
            if result[1]: ur_objs=unroll[0]
            else: ur_objs=Rhino.Geometry.Brep.JoinBreps(unroll[0],tol)
            ur_IDs=[sc.doc.Objects.AddBrep(ur_obj) for ur_obj in ur_objs]
            bb=rs.BoundingBox(ur_IDs)
            if x_extents>0:
                if bb[3].Y-bb[0].Y>max_y: max_y=bb[3].Y-bb[0].Y
                if bb[1].X-bb[0].X>x_extents:
                    x_extents=bb[1].X-bb[0].X
                    exceed_warning=True
                if new_sp.X+bb[1].X>(x_origin+x_extents):
                    #need to reset start point to x_origin, y_max
                    new_sp.X=x_origin
                    new_sp.Y+=max_y+result[3]
            move_vec=new_sp-bb[0]
            
            if unroll[1]:
                ur_crv_IDs=[sc.doc.Objects.AddCurve(ur_obj) for ur_obj in unroll[1]]
                ur_IDs.extend(ur_crv_IDs)
            if unroll[2]:
                ur_pt_IDs=[sc.doc.Objects.AddPoint(ur_obj) for ur_obj in unroll[2]]
                ur_IDs.extend(ur_pt_IDs)
            if unroll[3]:
                ur_dot_IDs=[sc.doc.Objects.AddTextDot(ur_obj) for ur_obj in unroll[3]]
                ur_IDs.extend(ur_dot_IDs)
            if result[2]:
                #keep properties (MatchAttributes() causes problems with grouping)
                TransferColorLayer(ur_IDs,brepIDs[i])
            if result[0]:
                #number objects and group
                AddDotToObjCtr(ur_IDs,str(ur_number),result[2])
                #add number dot to original object
                AddDotToObjCtr([brepIDs[i]],ur_number,result[2])
            #move all objs into position
            rs.MoveObjects(ur_IDs,move_vec)
            new_sp=(bb[1]+(move_vec+Rhino.Geometry.Vector3d(result[3],0,0)))
        else:
            no_unroll+=1
    
    #Clean up, store settings, report
    sc.sticky["MultiUR_Numbering"] = result[0]
    sc.sticky["MultiUR_Explode"] = result[1]
    sc.sticky["MultiUR_Properties"]=result[2]
    sc.sticky["MultiUR_Spacing"] = result[3]
    sc.sticky["MultiUR_XLimit"] = x_extents
    
    if exceed_warning:
        us=rs.UnitSystemName(abbreviate=True)
        msg="At least one of the unrolled objects exceeded the X extents limit!\n"
        msg+="Limit has been extended to {:.2f} {} ".format(x_extents,us)
        msg+="to allow all objects to unroll."
        rs.MessageBox(msg,48)
    msg="Sucessfully unrolled {} objects".format(len(brepIDs)-no_unroll)
    if no_unroll > 0:
        msg+=" | Unable to unroll {} objects".format(no_unroll)
    print msg

MultiUnroll()