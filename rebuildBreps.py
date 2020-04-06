import rhinoscriptsyntax as rs
import trkRhinoPy as trp

objs = rs.GetObjects("select objects", rs.filter.polysurface, preselect=True)

rs.EnableRedraw(False)
newbreps = map(trp.rebuildBrep, objs)
rs.UnselectAllObjects()
# rs.SelectObjects(newbreps)
rs.EnableRedraw(True)