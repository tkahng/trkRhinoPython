import rhinoscriptsyntax as rs
import trkRhinoPy as trp

crvs = rs.GetObjects("select crvs", rs.filter.curve, preselect=True)
dist = rs.GetReal("dist")

def Func(x):
    return trp.offsetInside(x, dist)

offsetcrvs = map(Func, crvs)
rs.UnselectObjects(crvs)
rs.SelectObjects(offsetcrvs)