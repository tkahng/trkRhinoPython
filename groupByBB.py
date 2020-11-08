"""
Groups objects by their containment within the set closed curves. 
Specifically groups along the x-axis, then sequentially sets a level attribute.
Used to sort and order objects in cad drawing context.
"""

import rhinoscriptsyntax as rs
import trkRhinoPy as trp
import scriptcontext as sc
# import json
# from _functools import reduce

objs = rs.GetObjects('select objects', preselect=True)

groupbb = rs.ObjectsByLayer('datums::planbb', False)

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

# def sortByAxis(objs, fn=lambda x:x[1].X, r=False):
#     pairs = map(objBBPtPair, objs)
#     sortedpairs = sorted(pairs, key=fn, reverse=r)
#     for idx, pairs in enumerate(sortedpairs, start=1):
#         rs.SetUserText(pairs[0], "level", str(idx))



# if rs.IsCurveClosed(curve) and rs.IsCurvePlanar(curve):
#     point = rs.GetPoint("Pick a point")
#     if point:
#         result = rs.PointInPlanarClosedCurve(point, curve)
#         if result==0: print "The point is outside of the closed curve."
#         elif result==1: print "The point is inside of the closed curve."
#         else: print "The point is on the closed curve."