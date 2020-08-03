# -*- coding: utf-8 -*-
import rhinoscriptsyntax as rs 
import trkRhinoPy as trp
import scriptcontext as sc
import json
import Rhino as rc
import ast

sc.doc = rc.RhinoDoc.ActiveDoc

src = sc.sticky["levels"]

levels = ast.literal_eval(src)

objs = rs.GetObjects('select objects', preselect=True)

# lvlel = map(lambda x: x['level'], x['elevation'], lvldict)

def getLvl(lvlname):
    lvl = [x for x in levels if x['level'] == lvlname]
    return lvl

def moveToLvl(obj):
    newlvl = getLvl(rs.GetUserText(obj, 'level'))
    newel = float(newlvl[0]['elevation'])
    # objlvl = rs.GetUserText(obj, 'level')
    # lvlkeys = rs.GetUserText(newlvl)
    # lvlvals = map(lambda x: rs.GetUserText(newlvl, x), lvlkeys)
    objel = trp.setObjZPair(obj)[1]

    # objel = float(rs.GetUserText(obj, 'elevation'))

    dist = newel - objel

    rs.MoveObject(obj, [0,0,dist])


def srfExtrude(srfs):
    rs.EnableRedraw(False)
    # for srf in srfs:
    rs.SelectObjects(srfs)
    rs.Command('_ExtrudeSrf _Pause')
    objs = rs.LastCreatedObjects()
    map(trp.copySourceLayer, objs, srfs)
    map(trp.copySourceData, objs, srfs)
    rs.EnableRedraw(True)

# srfExtrude(objs)

map(moveToLvl, objs)