import rhinoscriptsyntax as rs
import trkRhinoPy as trp

objs = rs.GetObjects('select objects', rs.filter.surface|rs.filter.polysurface, preselect=True)

rs.EnableRedraw(False)

if objs:
    map(trp.setObjAreaValue, objs)

rs.EnableRedraw(True)