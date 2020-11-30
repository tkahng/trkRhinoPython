import rhinoscriptsyntax as rs
import scriptcontext as sc
import trkRhinoPy as trp
# from trkRhinoPy import BrepFootPrintRegion
import Rhino

ids = rs.GetObjects("select polysrf", rs.filter.polysurface|rs.filter.surface, preselect=True)

rs.EnableRedraw(False)

breps = [rs.coercegeometry(id) for id in ids]

# boundary = trp.BrepFootPrintUnion(breps)

# for i in boundary:
#     sc.doc.Objects.AddCurve(i)


if rs.ExeVersion() == 7:
    boundary = trp.BrepFootPrintRegion(breps)
    silscrv = [sc.doc.Objects.AddCurve(sil) for sil in boundary]
    map(trp.setObjArea, silscrv)
    rs.UnselectAllObjects()
    rs.SelectObjects(silscrv)

elif rs.ExeVersion() == 6:
    sils = []
    for brep in breps:
        edges = brep.Edges
        edgecrvs = [e.DuplicateCurve() for e in edges]
        sils.extend(edgecrvs)
    # print sils
    silscrv = [sc.doc.Objects.AddCurve(sil) for sil in sils]
    rs.UnselectAllObjects()
    rs.SelectObjects(silscrv)
    rs.Command('_CurveBoolean AllRegions _Enter')
    rs.DeleteObjects(silscrv)

# elif rs.ExeVersion() == '7':
