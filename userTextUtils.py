# -*- coding: utf-8 -*-
import rhinoscriptsyntax as rs 

objs = rs.GetObjects('select srfs', rs.filter.surface, preselect=True)

def setSourceLayer(obj, source):
    sourceLayer = rs.ObjectLayer(source)
    rs.SetUserText(obj, 'source Layer', sourceLayer)

def copySourceLayer(obj, source):
    sourceLayer = rs.ObjectLayer(source)
    rs.ObjectLayer(obj, sourceLayer)

def getSourceKeys(source):
    if rs.IsUserText(source) == 0:
        print 'no keys'
        return
    return [ x for x in rs.GetUserText(source) if "BakeName" not in x ]

def sourceKeyValue(source):
    keys = getSourceKeys(source)
    values = map(lambda x: rs.GetUserText(source, x), keys)
    return keys, values

def copySourceData(obj, source):
    keyValue = sourceKeyValue(source)
    print keyValue
    map(lambda x, y: rs.SetUserText(obj, x, y), keyValue[0], keyValue[1])

def valuesFromLayer(obj):
    layer = rs.ObjectLayer(obj)
    if "::" in layer:
        layer = layer.split("::")
        layer = layer[1]
    keys = layer.split()
    return keys

def setValueByLayer(obj):
    keys = 'usage function'
    keys = keys.split()
    values = valuesFromLayer(obj)
    map(lambda x,y: rs.SetUserText(obj, x, y), keys, values)

def setAreaValue(obj):
    area = rs.SurfaceArea(obj)[0]
    area = round(area, 2)
    rs.SetUserText(obj, 'area', str(area))

def boolToggle(input):
    if len(input) == 0:
        return False
    else:
        return True
    
map(setValueByLayer, objs)
map(setAreaValue, objs)

    
# def srfExtrude(srfs):
#     # for srf in srfs:
#     rs.SelectObjects(srfs)
#     rs.Command('_ExtrudeSrf _Pause')
#     objs = rs.LastCreatedObjects()
#     map(copySourceLayer, objs, srfs)
#     map(copySourceData, objs, srfs)

# srfExtrude(objs)

# def swapParentLayer(obj, indx, newparent):
#     layer = rs.ObjectLayer(obj)
#     if "::" in layer:
#         splitlayer = layer.split("::")
#         return splitlayer[indx]
#     else:
#         return