import trkRhinoPy as trp
import rhinoscriptsyntax as rs
import rhinopythonscripts as rps
import Rhino
objs = rs.GetObjects()

rhobjlist = rps

sf = rps.RhinoObjectsToSmartFeatures(objs)

print sf[0].attributes