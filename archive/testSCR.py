import rhinoscriptsyntax as rs
import trkRhinoPy as trp

objs = rs.GetObjects("Select surfaces", rs.filter.surface, preselect=True)
rs.EnableRedraw(False)

def calcArea(srfs):
    areas = []
    for srf in srfs:
        areas.append(rs.SurfaceArea(srf)[0])
    totalArea = sum(areas)
    # totalAreaPy = totalArea/3.3058
    # print(area, areapy)
    # txt = rs.ClipboardText(area)
    return totalArea

siteKeys = ("site area", "legal scr", "legal far")

def getSiteCoverage(objs):
    designCoverageArea = calcArea(objs)
    return designCoverageArea

def runTest():
    areas = (createCoverage(objs), createFloors(objs))
    sitearea = float(rs.GetDocumentUserText("site area"))
    legalscr = float(rs.GetDocumentUserText("legal scr"))
    legalfar = float(rs.GetDocumentUserText("legal far"))
    designGFA = areas[1]
    designFAR = designGFA/sitearea
    designCVA = areas[0]
    designSCR = designCVA/sitearea
    rs.SetDocumentUserText("design gfa", str(round(designGFA, 2)))
    rs.SetDocumentUserText("design far", str(round(designFAR, 2)))
    rs.SetDocumentUserText("design cva", str(round(designCVA, 2)))
    rs.SetDocumentUserText("design scr", str(round(designSCR, 2)))