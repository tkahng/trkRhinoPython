# -*- coding: utf-8 -*-
import rhinoscriptsyntax as rs 
import trkRhinoPy as trp
import scriptcontext as sc
# import Rhino as rc

# sc.doc = rc.RhinoDoc.ActiveDoc

levels = sc.sticky["lvldict"]

objs = rs.GetObjects('select objects', rs.filter.surface|rs.filter.polysurface, preselect=True)

rs.EnableRedraw(False)

def massFromSrf(obj):
    lvl = levels[rs.GetUserText(obj, 'level')]
    height = float(lvl['height'])
    startpt = trp.objBBPts(obj)[0]
    endpt = (startpt.X, startpt.Y, startpt.Z + height)
    curve = rs.AddLine(startpt, endpt)
    mass = rs.ExtrudeSurface(obj, curve)
    trp.copySourceLayer(mass, obj)
    trp.copySourceData(mass, obj)
    rs.DeleteObject(curve)
    return mass

rs.UnselectAllObjects()

masses = map(massFromSrf, objs)

rs.SelectObjects(masses)

rs.EnableRedraw(True)