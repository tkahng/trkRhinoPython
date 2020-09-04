import rhinoscriptsyntax as rs

polySrfs = rs.GetObjects('select polysrfs', rs.filter.polysurface, preselect=True)
width = rs.GetReal("width", 0.2)
height = rs.GetReal("height", 3)

# if polySrf: 

def wallProfile(polySrf):

    if polySrf:
        offsets = []

        border = rs.DuplicateSurfaceBorder( polySrf )
        rs.SimplifyCurve(border)
        offsets.append(rs.OffsetCurve(border, [0,0,0], width/2))

        faces = rs.ExplodePolysurfaces(polySrf, False)
        faceborders = [rs.DuplicateSurfaceBorder(face) for face in faces]
        rs.DeleteObjects(faces)

        for faceborder in faceborders:
            rs.SimplifyCurve(faceborder)
            centroid = rs.CurveAreaCentroid(faceborder)
            offsets.append(rs.OffsetCurve(faceborder, centroid[0], width/2))

        rs.DeleteObjects(faceborders)

        srf = rs.AddPlanarSrf(offsets)

        rs.DeleteObjects(border)
        rs.DeleteObjects(offsets)
        return srf

def addRail(obj):
    if len(obj)>1:
        obj = obj[0]
        
    point1 = rs.EvaluateSurface(obj, 1, 0)
    vec = rs.CreateVector(0, 0, height)
    point2 = rs.CopyObject(point1, vec)
    line = rs.AddLine(point1, point2)
    if point2: rs.DeleteObjects(point2)
    return line


def makeWall(obj):
    rs.EnableRedraw(False)

    shape = wallProfile(obj)
    railCurve = addRail(shape)

    wall = rs.ExtrudeSurface(shape, railCurve)

    rs.DeleteObjects(shape)
    rs.DeleteObjects(railCurve)
    rs.EnableRedraw(False)
    return wall

if polySrfs:
    rs.SelectObjects([makeWall(polySrf) for polySrf in polySrfs if not rs.IsPolysurfaceClosed(polySrf)])