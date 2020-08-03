import rhinoscriptsyntax as rs
import trkRhinoPy as trp
import scriptcontext as sc
# import json
# from _functools import reduce

objs = rs.GetObjects('select objects', preselect=True)

# sortingAxis = rs

def objBBPtPair(obj):
    box = rs.BoundingBox(obj)
    minZ = box[0]
    maxZ = box[-2]
    mid = (box[0] + box[-2])/2
    return obj, mid, minZ, maxZ
    # rs.addpoint

def sortByAxis(objs, fn=lambda x:x[1].X, r=False):
    pairs = map(objBBPtPair, objs)
    sortedpairs = sorted(pairs, key=fn, reverse=r)
    for idx, pairs in enumerate(sortedpairs, start=1):
        rs.SetUserText(pairs[0], "level", str(idx))
        # rs.SetUserText(pairs[0], "level", str(idx))
        

# sortByAxis(objs, fn=lambda x:x[1].Y)
sortByAxis(objs, fn=lambda x:x[1].X)

# def objcentroid(obj):
#     box = rs.BoundingBox(obj)
#     minZ = box[0]
#     maxZ = box[-2]
#     mid = (minZ + maxZ)/2
#     rs.AddPoints([minZ, maxZ, mid])
#     # rs.addpoint

# def my_add(a, b):
#     result = (a + b)/2
#     rs.AddPoint(result)
#     return rs.AddPoint(result)

# def objBBPtPair(obj):
#     box = rs.BoundingBox(obj)
#     mid = (box[0] + box[-2])/2
#     return obj, mid
#     # rs.addpoint

# def sortByAxis(objs, fn=lambda x:x[1].X, r=False):
#     pairs = map(objBBPtPair, objs)
#     return sorted(pairs, key=fn, reverse=r)


# def setLevelforPlans(x, idx):
#     rs.SetUserText(x[0], "level", str(idx))
#     # rs.SetUserText(x[0], "grade", grade) 
#     # rs.SetUserText(x[0], "elevation", str(x[1]))
#     # setBrepHeight(x[0])

# def setPlanLevel(sortedpairs, isUG, func):
#     for idx, pairs in enumerate(sortedpairs, start=1):
#         map(lambda x: func(x, idx), pairs)


# def process(objs, func):


# # def pointreduce(obj):
# #     box = rs.BoundingBox(obj)
# #     reduce(my_add, box)

# map(objBBCentroid, objs)