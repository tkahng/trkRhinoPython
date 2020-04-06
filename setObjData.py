import rhinoscriptsyntax as rs
import trkRhinoPy as trp

objs = rs.GetObjects('select objects', preselect=True)

rs.EnableRedraw(False)

keys = 'usage function'

def Func(x):
    # trp.valuesFromLayer(x)
    trp.setValueByLayer(x,keys)
    trp.setSrfAreaValue(x)

def applyFunc(objs):
    map(Func, objs)

if objs:
    applyFunc(objs)

rs.EnableRedraw(True)