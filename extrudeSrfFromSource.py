# -*- coding: utf-8 -*-
import rhinoscriptsyntax as rs 
import trkRhinoPy as trp

objs = rs.GetObjects('select srfs', rs.filter.surface, preselect=True)

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