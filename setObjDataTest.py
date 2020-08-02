import rhinoscriptsyntax as rs
import trkRhinoPy as trp

objs = rs.GetObjects('select objects', preselect=True)

rs.EnableRedraw(False)

keys = 'usage func type'

def valuesFromLayer(obj):

    layer = rs.ObjectLayer(obj)
    if "::" in layer:
        layer = layer.split("::")
        layer = layer[-1]
    if " " in layer:
        values = layer.split(" ")
        return values
    else:
        return [layer]

def setValueByLayer(obj, keys):
    keys = keys.split()
    values = valuesFromLayer(obj)
#    values[1], values[-1] = values[-1], values[1]
    kv = zip(keys, values)
    map(lambda x: rs.SetUserText(obj, x[0], x[1]), kv)


def Func(x):
    valuesFromLayer(x)
    setValueByLayer(x,keys)
    trp.setObjAreaValue(x)
    trp.setBrepHeight(x)
    

def setClass(obj):
    classKeys = 'units public'
    try:
        func = rs.GetUserText(obj, "func")
        if func in classKeys:
            classValue = func
        else:
            classValue = "na"
        rs.SetUserText(obj, "class", classValue)
    except:
        return

def applyFunc(objs):
    map(Func, objs)
    map(setClass, objs)

if objs:
    applyFunc(objs)

'''class data'''




rs.EnableRedraw(True)