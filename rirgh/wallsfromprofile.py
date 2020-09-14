import clr
clr.AddReference('System.Core')
clr.AddReference('RhinoInside.Revit')
clr.AddReference('RevitAPI') 
clr.AddReference('RevitAPIUI')

from System import Enum

import rhinoscriptsyntax as rs
import Rhino
import Rhino.Geometry
import RhinoInside
import Grasshopper
from RhinoInside.Revit import Revit
from Autodesk.Revit import DB

clr.ImportExtensions(RhinoInside.Revit.Convert.Geometry)
doc = Revit.ActiveDBDocument

if 'generated_wall_id' not in globals():
    generated_wall_id = None

if P:
    P = rs.coercegeometry(P)
    lvloffset = P.GetBoundingBox(False).Min.Z
    print lvloffset
    curves = [x.ToLine() for x in list(P.ToPolyline().GetSegments())]
#    curves = [rs.coercegeometry(x).ToCurve() for x in P]
    print curves
    wall_type = doc.GetElement(DB.ElementId(T))
    level = doc.GetElement(DB.ElementId(L))
    lvlel = level.Parameter[DB.BuiltInParameter.LEVEL_ELEV].AsDouble() * Revit.ModelUnits
    off = lvloffset-lvlel
    print lvlel
    tg = DB.TransactionGroup(doc, 'group')
    tg.Start()
    
    t = DB.Transaction(doc, 'Create Wall from Profile')
    t.Start()
    if generated_wall_id:
        doc.Delete(generated_wall_id)
    new_wall = None
    print(curves, wall_type.Id, level.Id, ST)
    new_wall = DB.Wall.Create(doc, curves, wall_type.Id, level.Id, ST)
    if new_wall:
        generated_wall_id = new_wall.Id
#        new_wall.Parameter[DB.BuiltInParameter.WALL_BASE_OFFSET].Set(lvloffset-lvlel)
        W = new_wall
    else:
        generated_wall_id = None
    t.Commit()
    
    t = DB.Transaction(doc, 'set offset')
    t.Start()
    W.Parameter[DB.BuiltInParameter.WALL_BASE_OFFSET].Set(off/Revit.ModelUnits)
    t.Commit()
    tg.Assimilate()