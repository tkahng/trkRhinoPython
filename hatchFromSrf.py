import rhinoscriptsyntax as rs
import trkRhinoPy as trp

objs = rs.GetObjects("Select a srf", rs.filter.surface, preselect=True)

rs.EnableRedraw(False)

def createHatch(obj):
    hatch = trp.hatchFromSrf(obj)
    trp.copySourceLayer(hatch, obj)
    return hatch
rs.UnselectObjects(objs)
hatches = map(createHatch, objs)
rs.SelectObjects(hatches)
group = rs.AddGroup()
rs.AddObjectsToGroup(hatches, group)
rs.EnableRedraw(True)