# -*- coding: utf-8 -*-
import rhinoscriptsyntax as rs 
import trkRhinoPy as trp
import scriptcontext as sc
# import Rhino as rc

# sc.doc = rc.RhinoDoc.ActiveDoc

levels = sc.sticky["lvldict"]

objs = rs.GetObjects('select objects', preselect=True)

rs.EnableRedraw(False)

def moveToLvl(obj):
    newlvl = levels[rs.GetUserText(obj, 'level')]
    newel = float(newlvl['elevation'])
    objel = trp.setObjZPair(obj)[1]
    dist = newel - objel
    rs.MoveObject(obj, [0,0,dist])

def setToLvlHeight(obj):
    newlvl = levels[rs.GetUserText(obj, 'level')]
    newheight = float(newlvl['height'])
    objz = trp.brepGetZ(obj)
    try:
        factor = newheight/objz[2]
        rs.SetUserText(obj, 'height', round(newheight, 3))
    except:
        return
    # rs.SetUserText(obj, 'height', round(newheight, 3))
    xform = rs.XformScale((1.0,1.0,factor), (0,0,objz[0]))
    rs.TransformObjects(obj, xform)

def func(x):
    moveToLvl(x)
    setToLvlHeight(x)

map(func, objs)

rs.EnableRedraw(True)