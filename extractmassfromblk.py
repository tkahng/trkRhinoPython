# -*- coding: utf-8 -*-
import rhinoscriptsyntax as rs 
import trkRhinoPy as trp
import scriptcontext as sc
import Rhino
# import Rhino as rc

# sc.doc = rc.RhinoDoc.ActiveDoc

# levels = sc.sticky["lvldict"]

blkids = rs.GetObjects('select objects', rs.filter.instance, preselect=True)

rs.EnableRedraw(False)

rs.UnselectAllObjects()

masses = []

def blkObjs(blkid):
    blockName = rs.BlockInstanceName(blkid)
    # objref = rs.coercerhinoobject(blkid)
    # idef = objref.InstanceDefinition
    # idefIndex = idef.Index
    
    # lvl = levels[rs.GetUserText(blkid, 'level')]
    # height = lvl['height']
    xform = rs.BlockInstanceXform(blkid)
    # objects = [x for x in rs.BlockObjects(blockName) if 'mass' in rs.ObjectLayer(x)]
    objects = filter(lambda x: 'mass' in rs.ObjectLayer(x), rs.BlockObjects(blockName))
    # objects = filter(lambda x: 'mass' in rs.ObjectLayer(x) and rs.GetUserText(x, 'class') != 'na', rs.BlockObjects(blockName))
    # objects = map(lambda x: rs.SetUserText(x, 'level', lvl), objects)
    # map(lambda x: rs.SetUserText(x, 'height', lvl))

    blockInstanceObjects = rs.TransformObjects(objects, xform, True)
    masses.extend(blockInstanceObjects)

map(blkObjs, blkids)
# masses = map(massFromSrf, objs)



rs.SelectObjects(masses)

rs.EnableRedraw(True)