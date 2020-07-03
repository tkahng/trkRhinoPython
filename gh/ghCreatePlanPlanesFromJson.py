import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino as rc
import json

sc.doc = rc.RhinoDoc.ActiveDoc

planplanes = x

sc.sticky["planplanes"] = map(json.loads, planplanes)
rs.SetDocumentUserText("planplanes", json.dumps(map(json.loads, planplanes)))