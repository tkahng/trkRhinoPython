# -*- coding: utf-8 -*-
import rhinoscriptsyntax as rs 
import trkRhinoPy as trp
import scriptcontext as sc

objs = rs.GetObjects('select srfs', rs.filter.surface, preselect=True)

levels = sc.sticky["levels"]

def getLvl(lvlname):
    lvl = [x for x in levels if x['level'] == lvlname]
    return lvl

def moveToLvl(obj, lvl):
    newlvl = getLvl(rs.GetUserText(obj, 'level'))
    # objlvl = rs.GetUserText(obj, 'level')
    lvlkeys = rs.GetUserText(newlvl)
    lvlvals = map(lambda x: rs.GetUserText(newlvl, x), lvlkeys)
    
    new


def srfExtrude(srfs):
    rs.EnableRedraw(False)
    # for srf in srfs:
    rs.SelectObjects(srfs)
    rs.Command('_ExtrudeSrf _Pause')
    objs = rs.LastCreatedObjects()
    map(trp.copySourceLayer, objs, srfs)
    map(trp.copySourceData, objs, srfs)
    rs.EnableRedraw(True)

srfExtrude(objs)