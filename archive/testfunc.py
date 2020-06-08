# -*- coding: utf-8 -*-
import rhinoscriptsyntax as rs
import trkRhinoPy as trp
import json
import ast

objs = rs.GetObjects('select objects', rs.filter.polysurface, preselect=True)

rs.EnableRedraw(False)

schema = {
'keys' : 'usage function',
'skeys' : 'function',
'svals' : 'unit public',
'classkey' : 'class',
'classvals' : 'rent na'
}

keylist = [schema['skeys'], schema['svals']]

def createKVByVal(obj, skeys, svals, classkey, classvals):
    objsval = rs.GetUserText(obj, skeys)
    svals = svals.split()
    classvals = classvals.split()
    if objsval not in svals:
        objclass = classvals[1]
    else:
        objclass = classvals[0]
    rs.SetUserText(obj, classkey, objclass)

def setObjDict(obj):
    rs.SetUserText(obj, 'objdict')
    objkeys = [ x for x in rs.GetUserText(obj) if "BakeName" not in x ]
    # objkeys = rs.GetUserText()
    # keys = 'level grade elevation'
    # keys = keys.split()
    objvals = map(lambda x: rs.GetUserText(obj, x), objkeys)
    # vals = [idx, grade, str(x[1])]
    # objdict = dict(zip(objkeys, objvals))
    # rs.SetUserText(obj, 'objdict')
    rs.SetUserText(obj, 'objdict', dict(zip(objkeys, objvals)))

docLvlDB = {}

def getObjDict(obj):
    userstr = rs.GetUserText(obj, "objdict")
    objdict = ast.literal_eval(userstr)
    docLvlDB[key] = objdict

def func(x):
    trp.setValueByLayer(x,schema['keys'])
    trp.setBrepHeight(x)
    trp.setObjAreaValue(x)
    createKVByVal(x, schema['skeys'], schema['svals'], schema['classkey'], schema['classvals'])
    setObjDict(x)
    # trp.setSrfAreaValue(x)

map(func, objs)

# def setBrepHeight(obj):
#     height = trp.brepGetZ(obj)
#     height = height[2]
#     rs.SetUserText(obj, "height", str(height))

# def setBrepFA(obj):
#     faces = trp.getBottomFace(obj)
#     area = trp.calcArea(faces)
#     rs.SetUserText(obj, "area", str(area[0]))
#     rs.SetUserText(obj, "areapy", str(area[1]))
#     rs.DeleteObjects(faces)

# objs = rs.GetObjects('select objects', preselect=True)

# def Func(x):
#     # trp.valuesFromLayer(x)
#     trp.setValueByLayer(x,keys)
#     trp.setSrfAreaValue(x)

# def applyFunc(objs):
#     map(Func, objs)

# if objs:
#     applyFunc(objs)

# objs = rs.GetObjects('select objs', rs.filter.surface|rs.filter.curve|rs.filter.point|rs.filter.polysurface, preselect=True)
# grade = rs.GetString("toggle grade")

# def process(objs, grade, func):
#     isUG = trp.boolToggle(grade)
#     groups = trp.groupByElevation(objs, isUG)
#     trp.setLevel(groups, isUG, func)

# if __name__ == '__main__':
#     process(objs, grade, trp.setLevelforObj)  

rs.EnableRedraw(True)