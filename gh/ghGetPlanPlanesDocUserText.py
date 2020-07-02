import rhinoscriptsyntax as rs
# import scriptcontext as sc
#import Rhino as rc
import ast
#import json

#sc.doc = rc.RhinoDoc.ActiveDoc

objdict = ast.literal_eval(rs.GetDocumentUserText("planplanes"))
# sticky = sc.sticky["levels"]
print objdict

keys = ['level', 'point']

def func(key):
    val = [d[key] for d in objdict]
    return val

level, point = map(func, keys)

x, y, z = map(lambda x:[d[x] for d in point], ['X', 'Y', 'Z'])

plane = map(lambda x:rs.CreatePlane(x), zip(x,y,z))