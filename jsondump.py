# -*- coding: utf-8 -*-
"""Exports a json file with each json object containing the key/value pair of each object from selection."""

import rhinoscriptsyntax as rs
import trkRhinoPy as trp
import json
import ast

# objs = rs.GetObjects('select objects', rs.filter.polysurface, preselect=True)
objs = rs.GetObjects('select objects', preselect=True)

def createObjDict(obj):
    # rs.SetUserText(obj, 'objdict')
    objkeys = [ x for x in rs.GetUserText(obj) if "BakeName" not in x ]
    objvals = map(lambda x: rs.GetUserText(obj, x), objkeys)
    return dict(zip(objkeys, objvals))
    # rs.SetUserText(obj, 'objdict', dict(zip(objkeys, objvals)))

dataStore = map(createObjDict, objs)

filter = "JSON File (*.json)|*.json|All Files (*.*)|*.*||"
filename = rs.SaveFileName("Save JSON file as", filter)

# If the file name exists, write a JSON string into the file.
if filename:
    # Writing JSON data
    with open(filename, 'w') as f:
        json.dump(dataStore, f)

# def getObjDict(obj):
#     userstr = rs.GetUserText(obj, "objdict")

#     objdict = ast.literal_eval(userstr)
#     return objdict

# def func(x):
#     # trp.setValueByLayer(x,schema['keys'])
#     # trp.setBrepHeight(x)
#     # trp.setObjAreaValue(x)
#     # createKVByVal(x, schema['skeys'], schema['svals'], schema['classkey'], schema['classvals'])
#     # setObjDict(x)
#     # trp.setSrfAreaValue(x)
#     return getObjDict(x)

# objsList = map(func, objs)
# objsDict = {}

# objsDict['objs'] = objsList

# # print type(objsDict)
# # print objsDict['objs'][0]
# # print type(objsList[0])
# # print objsList[0]
# # print(len(objsDict['objs'][0]))

# filter = "JSON File (*.json)|*.json|All Files (*.*)|*.*||"
# filename = rs.SaveFileName("Save JSON file as", filter)

# # If the file name exists, write a JSON string into the file.
# if filename:
#     # Writing JSON data
#     with open(filename, 'w') as f:
#         json.dump(objsDict, f)