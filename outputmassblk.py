# -*- coding: utf-8 -*-
import rhinoscriptsyntax as rs 
import trkRhinoPy as trp
import scriptcontext as sc
# import Rhino as rc

# sc.doc = rc.RhinoDoc.ActiveDoc

levels = sc.sticky["lvldict"]

blkid = rs.GetObject('select objects', rs.filter.instance, preselect=True)

rs.EnableRedraw(False)

def swapParentLayer(obj):
    layer = rs.ObjectLayer(obj)
    if "::" in layer:
        splitlayer = layer.split("::")
        currentParent = splitlayer[0]
        newlayer = layer.replace(currentParent, 'output mass 2')
        rs.ObjectLayer(obj, newlayer)

def blkObjs(blkid):
    name = rs.BlockInstanceName(blkid)
    lvl = levels[rs.GetUserText(blkid, 'level')]
    height = float(lvl['height'])
    xform = rs.BlockInstanceXform(blkid)
    objs = rs.BlockObjects(name)
    masses = map(lambda x: massFromSrf(x, height), objs)
    # newblk = rs.AddBlock(masses, (0,0,0), name=name, delete_input=True)
    rs.TransformObjects(masses, xform)
    return objs

def massFromSrf(obj, height):
    # lvl = levels[rs.GetUserText(obj, 'level')]
    # height = float(lvl['height'])
    startpt = trp.objBBPts(obj)[0]
    endpt = (startpt.X, startpt.Y, startpt.Z + height)
    curve = rs.AddLine(startpt, endpt)
    mass = rs.ExtrudeSurface(obj, curve)
    
    trp.copySourceLayer(mass, obj)
    # trp.copySourceData(mass, obj)
    swapParentLayer(mass)
    rs.DeleteObject(curve)
    return mass

# rs.UnselectAllObjects()

blkObjs(blkid)

# masses = map(massFromSrf, objs)



# rs.SelectObjects(masses)

rs.EnableRedraw(True)