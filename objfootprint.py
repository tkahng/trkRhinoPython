import rhinoscriptsyntax as rs
import scriptcontext as sc
import trkRhinoPy as trp
import Rhino

ids = rs.GetObjects("select polysrf", rs.filter.polysurface|rs.filter.surface, preselect=True)

rs.EnableRedraw(False)

breps = [rs.coercegeometry(id) for id in ids]

# boundary = trp.BrepFootPrintUnion(breps)

# for i in boundary:
#     sc.doc.Objects.AddCurve(i)

sils = []

for brep in breps:
    edges = brep.Edges
    edgecrvs = [e.DuplicateCurve() for e in edges]
    sils.extend(edgecrvs)
print sils

if rs.ExeVersion() == '6':
    silscrv = [sc.doc.Objects.AddCurve(sil) for sil in sils]
    rs.UnselectAllObjects()
    rs.SelectObjects(silscrv)
    rs.Command('_CurveBoolean AllRegions _Enter')
    rs.DeleteObjects(silscrv)

# elif rs.ExeVersion() == '7':
