import rhinoscriptsyntax as rs
import trkRhinoPy as trp

objs = rs.GetObjects('select objects', rs.filter.polysurface, preselect=True)

def func(obj):
    height = trp.brepGetZ(obj)
    rs.SetUserText(obj, "height", str(height))

map(func, objs)