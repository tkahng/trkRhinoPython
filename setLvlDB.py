# -*- coding: utf-8 -*-
import rhinoscriptsyntax as rs
import trkRhinoPy as trp
import scriptcontext as sc
import json

objs = rs.GetObjects('select objs', rs.filter.surface|rs.filter.curve|rs.filter.point|rs.filter.polysurface, preselect=True)

levels = map(trp.createObjDict, objs)

sc.sticky["levels"] = json.dumps(levels)
rs.SetDocumentUserText("levels", json.dumps(levels))


