# -*- coding: utf-8 -*-
import rhinoscriptsyntax as rs 
import trkRhinoPy as trp
import scriptcontext as sc
import Rhino
# import Rhino as rc

# sc.doc = rc.RhinoDoc.ActiveDoc

levels = sc.sticky["lvldict"]

blkid = rs.GetObject('select objects', rs.filter.instance, preselect=True)

rs.EnableRedraw(False)

# def swapParentLayer(obj):
#     layer = rs.ObjectLayer(obj)
#     if "::" in layer:
#         splitlayer = layer.split("::")
#         currentParent = splitlayer[0]
#         newlayer = layer.replace(currentParent, 'output mass 2')
#         rs.ObjectLayer(obj, newlayer)
# class 


def blkObjs(blkid):
    blockName = rs.BlockInstanceName(blkid)
    objref = rs.coercerhinoobject(blkid)
    idef = objref.InstanceDefinition
    idefIndex = idef.Index
    
    lvl = levels[rs.GetUserText(blkid, 'level')]
    height = float(lvl['height'])
    xform = rs.BlockInstanceXform(blkid)
    objects = [x for x in rs.BlockObjects(blockName) if rs.IsSurface(x)]

    masses = map(lambda x: massFromSrf(x, height), objects)
    # masses = map(lambda x: rs.SetUserText(x, 'blkname', blockName), masses)
    # newblk = rs.AddBlock(masses, (0,0,0), name=name, delete_input=True)

    objects.extend(masses)

    newGeometry = []
    newAttributes = []
    for object in objects:
        newGeometry.append(rs.coercegeometry(object))
        ref = Rhino.DocObjects.ObjRef(object)
        attr = ref.Object().Attributes
        attr.SetUserString('blkname', blockName)
        newAttributes.append(attr)
    
    InstanceDefinitionTable = sc.doc.ActiveDoc.InstanceDefinitions
    InstanceDefinitionTable.ModifyGeometry(idefIndex, newGeometry, newAttributes)
    # rs.TransformObjects(masses, xform)
    rs.DeleteObjects(masses)
    # return objs

def massFromSrf(obj, height):
    # lvl = levels[rs.GetUserText(obj, 'level')]
    # height = float(lvl['height'])
    startpt = trp.objBBPts(obj)[0]
    endpt = (startpt.X, startpt.Y, startpt.Z + height)
    curve = rs.AddLine(startpt, endpt)
    mass = rs.ExtrudeSurface(obj, curve)
    
    trp.copySourceLayer(mass, obj)
    rs.SetUserText(mass, str(height))
    # trp.copySourceData(mass, obj)
    swapParentLayer(mass)
    rs.DeleteObject(curve)
    return mass

# rs.UnselectAllObjects()

blkObjs(blkid)

# masses = map(massFromSrf, objs)



# rs.SelectObjects(masses)

rs.EnableRedraw(True)