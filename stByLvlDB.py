import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino as rc
import json

# sc.doc = rc.RhinoDoc.ActiveDoc
levels = rs.GetDocumentUserText("levels")
# print type(levels)

#datastore = sc.sticky["levels"]
#print type(datastore)

datastore = json.loads(levels)

data = []

# def groupByElevation(pairs):
# #    pairs = map(setObjZPair, objs)
#     values = set(map(lambda x:x[1], pairs))
#     newpairs = [[y for y in pairs if y[1]==x] for x in values]
#     return sorted(newpairs, key=lambda x:x[0][1])

# sorteddata = map(lambda y:sorted(y, key=lambda x:x[0][1]), data)


for lvl in datastore:
    pair = [float(lvl.get("level")), float(lvl.get("elevation"))]
    data.append(pair)


str = "stCreate _Enter _Enter " & Rhino.Pt2Str(arrPt) & " _Enter"