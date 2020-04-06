# -*- coding: utf-8 -*-
import rhinoscriptsyntax as rs
import ast

objs = rs.GetObjects('select objs', rs.filter.surface|rs.filter.curve|rs.filter.point, preselect=True)
# grade = rs.GetString("toggle grade")


docLvlDB = {}

def getObjDict(obj):
    userstr = rs.GetUserText(obj, "lvldict")
    objdict = ast.literal_eval(userstr)
    key = str(objdict["level"])
    docLvlDB[key] = objdict


def setDocLvlDB():
    map(getObjDict, objs)
    docval = str(docLvlDB)
    rs.SetDocumentUserText("docLvlDB", docval)

# def getObjDict(obj):
#     userstr = rs.GetUserText(obj, "lvldict")
#     objdict = ast.literal_eval(userstr)
#     key = str(objdict["level"])
#     return key, objdict


# def createDocLvlDB(objs):
#     docLvlDB = {}
#     objkv = map(getObjDict, objs)
#     map(docLvlDB.update, objkv)
#     docval = str(docLvlDB)
#     rs.SetDocumentUserText("docLvlDB", docval)

# createDocLvlDB(objs)

setDocLvlDB()


