import rhinoscriptsyntax as rs
import trkRhinoPy as trp
import scriptcontext as sc
import Rhino as rc
#import ast
import json

sc.doc = rc.RhinoDoc.ActiveDoc

print objs

def process(objs, isUG, func):
    
    groups = trp.groupByElevation(objs, isUG)
    trp.setLevel(groups, isUG, func)
    levels = [trp.createObjDict(x[0][0]) for x in groups]
    sc.sticky["levels"] = json.dumps(levels)
    rs.SetDocumentUserText("levels", json.dumps(levels))

process(objs, isUG, trp.setLevelforDatum) 