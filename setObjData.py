import rhinoscriptsyntax as rs
import trkRhinoPy as trp

objs = rs.GetObjects('select objects', preselect=True)

rs.EnableRedraw(False)

keys = 'usage func'

def Func(x):
    # trp.valuesFromLayer(x)
    trp.setValueByLayer(x,keys)
    # trp.setSrfAreaValue(x)

def setClass(obj):
    classKeys = 'units public'
    func = rs.GetUserText(obj, "func")
    if func in classKeys:
        classValue = func
    else:
        classValue = "na"
    rs.SetUserText(obj, "class", classValue)

def applyFunc(objs):
    map(Func, objs)
    map(setClass, objs)

if objs:
    applyFunc(objs)


'''class data'''




rs.EnableRedraw(True)