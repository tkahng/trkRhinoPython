#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Finds and selects "near-duplicate" curves within a user-set tolerance.
Currently there is a bug in CurveDeviation (GetDistancesBetweenCurves)
that makes it unreliable...  So this script instead uses first a
bounding box check, then length check, then divides curve and checks individual
point deviations.  Short-circuit logic if one of the tests fail. Status bar 
indicator for progress, can be long with large numbers of curves.
Script by Mitch Heynick 24.10.17
Revised - added optional arguments - and localized FR/EN 03.11.17
Minor adaptation 11.07.19: time rounded to 0.01 sec., default sampling set to 25 

To do: revise with an rTree? Separate out polylines as different procedure?"""

import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino, clr, System, time
import Rhino.RhinoMath as rm

def Localize(local_id):
    #pass rs.LocaleID() as argument
    msgs=[]
    if local_id==1036:
        msgs.append("Sélectionner les courbes à analyser")
        msgs.append("Tolérance de sélection")
        msgs.append("Calcul...")
        msgs.append("Calcul")
        msgs.append("Temps écoulé: {:.2f}")
        msgs.append("{} courbes quasi-doublons trouvées")
        msgs.append("Aucun quasi-doublon trouvé dans la tolérance choisi")
    else:
        msgs.append("Select curves to process")
        msgs.append("Selection tolerance")
        msgs.append("Working...")
        msgs.append("Processing")
        msgs.append("Elapsed time: {:.2f}")
        msgs.append("{} near duplicate curves found")
        msgs.append("No near duplicates found within tolerance")
    return msgs

def PC(): return Rhino.Runtime.HostUtils.RunningOnWindows

def IsNearDupCrv(ref_crv,test_crv,user_tol,divs=5):
    #ref_crv, test_crv are tuples: [0]=crv,[1]=bb,[2]=len
    if ref_crv[1].Max.EpsilonEquals(test_crv[1].Max,user_tol):
        if ref_crv[1].Min.EpsilonEquals(test_crv[1].Min,user_tol):
            #bounding box within tolerance, test overall length
            if rm.EpsilonEquals(ref_crv[2],test_crv[2],user_tol):
                #length within tolerance, divide ref. curve by a # of points
                pt_cont=clr.StrongBox[System.Array[Rhino.Geometry.Point3d]]()
                div=ref_crv[0].DivideByCount(divs,True,pt_cont)
                #check point deviation at each point
                if div:
                    #pt_cont.Value is list of points on ref_crv
                    for pt in pt_cont.Value:
                        rc,p=test_crv[0].ClosestPoint(pt)
                        if rc:
                            if pt.DistanceTo(test_crv[0].PointAt(p))>user_tol:
                                #at least one point is too far, jump out
                                return
                    return True

#can adapt sampling (crv_divs)
def SelectNearDupCrvs(chk_all=True,sel_dup_all=False,crv_divs=25,user_tol=0.1):
    msgs=Localize(rs.LocaleID())
    if chk_all:
        crvIDs=rs.ObjectsByType(4,state=1)
    else:
        crvIDs=rs.GetObjects(msgs[0],4,preselect=True)
    if not crvIDs: return
    
    if "SelNearDup_Tol" in sc.sticky: user_tol = sc.sticky["SelNearDup_Tol"]
    
    tol=sc.doc.ModelAbsoluteTolerance
    comp_tol=rs.GetReal(msgs[1],user_tol,minimum=tol)
    if comp_tol is None: return
    
    crv_bbs=[]
    for crvID in crvIDs:
        crv=sc.doc.Objects.Find(crvID).Geometry
        bb=crv.GetBoundingBox(True)
        length=crv.GetLength()
        crv_bbs.append((crv,bb,length))
        
    rs.EnableRedraw(False)
    rs.Prompt(msgs[2])
    if PC: rs.StatusBarProgressMeterShow(msgs[3],0,100,True)
    #idea - collect indices, not IDs...
    found_index=set()
    st=time.time()
    for i in range(len(crv_bbs)-1):
        if PC and i % 100 ==0:
            rs.StatusBarProgressMeterUpdate(100*i/len(crv_bbs))
        for j in range(i+1,len(crv_bbs)):
            #check to see if cuve is already in select list
            if j in found_index: continue
            #print "Compare curve {} to curve {}".format(i,j)
            if IsNearDupCrv(crv_bbs[i],crv_bbs[j],comp_tol,crv_divs):
                found_index.add(j)
                if sel_dup_all: found_index.add(i)
    if PC: rs.StatusBarProgressMeterHide()
    print msgs[4].format(time.time()-st)
    if found_index:
        #need to add list of IDs
        found=[crvIDs[index] for index in found_index]
        rs.SelectObjects(found)
        msg=msgs[5].format(len(found))
    else:
        msg=msgs[6]
    print msg
    sc.sticky["SelNearDup_Tol"] = comp_tol
"""optional arguments:
chk_all - True==check all visible selectable curves; False==user select curves
sel_dup_all - True==select all duplicates, False==leave one duplicate unselected
crv_divs - number of points to sample along curve
user_tol - default comparison tolerance (user-adaptable, sticky)
Defaults: True, False, 25, 0.1 """
SelectNearDupCrvs()