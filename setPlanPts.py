import rhinoscriptsyntax as rs
import trkRhinoPy as trp
import scriptcontext as sc
import json

# levels = sc.sticky["lvldict"]
objs = rs.GetObjects('select objects', rs.filter.point, preselect=True)
# def objBBPtPair(obj):
#     box = rs.BoundingBox(obj)
#     minZ = box[0]
#     maxZ = box[-2]
#     mid = (box[0] + box[-2])/2
#     return obj, mid, minZ, maxZ
#     # rs.addpoint

def objPtPair(obj):
    return obj, rs.CreatePoint(obj)

def sortByAxis(objs, fn=lambda x:x[1].X, r=False, key='level', start=1):
    kv = []
    kv2 = []
    pairs = map(objPtPair, objs)
    sortedpairs = sorted(pairs, key=fn, reverse=r)
    for idx, pairs in enumerate(sortedpairs, start=start):
        rs.SetUserText(pairs[0], key, str(idx))
        kv.append((str(idx), pairs[1]))
        kv2.append((str(idx), (pairs[1].X, pairs[1].Y, pairs[1].Z)))
    planptdict = dict(kv)
    rs.SetDocumentUserText("planpts", json.dumps(dict(kv2)))
    sc.sticky['planptdict'] = planptdict

sortByAxis(objs)