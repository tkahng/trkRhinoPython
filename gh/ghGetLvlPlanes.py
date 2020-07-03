import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino as rc
import ast
#import json

sc.doc = rc.RhinoDoc.ActiveDoc

src = sc.sticky["levels"] if sticky else rs.GetDocumentUserText("levels")

objdict = ast.literal_eval(src)

keys = ['height', 'grade', 'elevation', 'level']

def func(key):
    val = [d[key] for d in objdict]
    return val

height, grade, elevation, level = map(func, keys)

plane = [rs.CreatePlane((0,0,float(x))) for x in elevation]