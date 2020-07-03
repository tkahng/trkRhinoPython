import rhinoscriptsyntax as rs
import trkRhinoPy as trp
import scriptcontext as sc
import json
import Rhino as rc
# import collections

sc.doc = rc.RhinoDoc.ActiveDoc

def createPtDict(pt):
    ptkeys = ["X","Y","Z"]
    ptVals = [pt.X, pt.Y, pt.Z]
    return dict(zip(ptkeys, ptVals))

def createLvlDict(pt, lvl):
    ptdict = createPtDict(pt)
    planekeys = ["level", "point"]
    planevals = [lvl, ptdict]
    lvldict = dict(zip(planekeys, planevals))
    return lvldict

planplanes = map(lambda x, y:createLvlDict(x, y), point, level)

sc.sticky["planplanes"] = planplanes
rs.SetDocumentUserText("planplanes", json.dumps(planplanes))