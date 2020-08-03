import trkRhinoPy as trp
import rhinoscriptsyntax as rs
from rhinopythonscripts.GeomTools import getSelected
import scriptcontext as sc
from rhinopythonscripts import Smart
import Rhino as rc
import json
import ast
from _functools import reduce

objs = rs.GetObjects('select objects', preselect=True)

groupbb = rs.ObjectsByLayer('planbb', False)

def objBBPtPair(obj):
    box = rs.BoundingBox(obj)
    mid = (box[0] + box[-2])/2
    return obj, mid


def groupByBB(objs):
    pairs = map(objBBPtPair, objs)

    for bb in groupbb:
        lvl = rs.GetUserText(bb, 'level')
        for pair in pairs:
            result = rs.PointInPlanarClosedCurve(pair[1], bb)
            if result==1:
                rs.SetUserText(pair[0], "level", lvl)

groupByBB(objs)

#objs = rs.GetObjects('select objects', preselect=True)
#
#def objBBPtPair(obj):
#    box = rs.BoundingBox(obj)
#    mid = (box[0] + box[-2])/2
#    return obj, mid
#    # rs.addpoint
#
#def sortByAxis(objs, fn=lambda x:x[1].X, r=False):
#    pairs = map(objBBPtPair, objs)
#    sortedpairs = sorted(pairs, key=fn, reverse=r)
#    for idx, pairs in enumerate(sortedpairs, start=1):
#        rs.SetUserText(pairs[0], "level", str(idx))
#
#sortByAxis(objs, fn=lambda x:x[1].Y)






#obj = rs.GetObject('select objects', preselect=True)
#
#box = rs.BoundingBox(obj)
#
#
#
##print box
#
#
#def my_add(a, b):
##    print a, b
#    result = (a + b)
##    rs.AddPoint(result)
#    return result
#
#a = reduce(my_add, box)
#print a
##sc.doc = rc.RhinoDoc.ActiveDoc
##
##src = sc.sticky["levels"]
##
##lvldict = ast.literal_eval(src)
##
##lvlk = [x['level'] for x in lvldict]
##
##newdict = dict(zip(lvlk, lvldict))
##
##newdict2 = dict(map(lambda x: zip(x['level'], x), lvldict))
###lvlel = map(lambda x: zip(x['level'], x['elevation']), lvldict)
##
###lvlk = [x['level'] for x in lvldict]
###lvlk = [x['lelevation'] for x in lvldict]
##
###print lvlk, lvll
##print newdict2
##print newdict
##print lvlk
##print lvldict
###print type(lvlel)
##
#### objs = rs.GetObjects()
###targId = rs.GetObject("Select the first object to replace")
####if not targId:return
###
###rhobj = sc.doc.Objects.Find(targId)
####geo = obj.Geometry
###
###
###rhobjlist = getSelected()
###
###sf = Smart.RhinoObjectsToSmartFeatures(rhobjlist)
###
###print sf[0].attributes
###
#### import Rhino.Geometry
#### import Grasshopper as gh
###
#### gh.tree
###
#### import 
#### rs.GetObject()
