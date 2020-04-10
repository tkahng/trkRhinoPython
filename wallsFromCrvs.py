import rhinoscriptsyntax as rs
# !-RunPythonScript "wallsFromCrvs.py"

objs = rs.GetObjects("Pick curves to loft", rs.filter.curve, preselect=True)
width = rs.GetReal("width", 0.4)
height = rs.GetReal("height", 3)
plane = rs.ViewCPlane()



def wallBaseSrf(crv, width):
    rs.SimplifyCurve(crv)
    if rs.IsCurveClosed(crv):
        domain = rs.CurveDomain(crv)
        parameter = (domain[0] + domain[1])/2.0
        rs.CurveSeam( crv, parameter )
    offsets = map(lambda x: rs.OffsetCurve( crv, [0,0,0], x), [width/2, -width/2])
    section = rs.AddLoftSrf(offsets,loft_type=2)

    if offsets: rs.DeleteObjects(offsets)
    if rs.IsPolysurface(section):
        return rs.ExplodePolysurfaces(section, delete_input=True)
    return section


def makeBrep(srf):
    point1 = rs.EvaluateSurface(srf, 0, 0)
    vec = rs.CreateVector(0, 0, height)
    point2 = rs.CopyObject(point1, vec)
    line = rs.AddLine(point1, point2)
    brep = rs.ExtrudeSurface(srf, line)
    if point2: rs.DeleteObjects(point2)
    if line: rs.DeleteObjects(line)
    return brep



# def makeBrep(srf):
#     rail = addRail(srf)
#     brep = rs.ExtrudeSurface(srf, rail)
#     if rail: rs.DeleteObjects(rail)
#     return brep

def makeWall(crv):
    srfs = wallBaseSrf(crv, width)
    breps = map(makeBrep, srfs)
    if srfs: rs.DeleteObjects(srfs)
    rs.SelectObjects(breps)
    return breps

rs.EnableRedraw(False)

if objs:
    rs.UnselectObjects(objs)

map(makeWall, objs)




rs.EnableRedraw(True)


        
# def addRail(obj):
#     pt1 = rs.EvaluateSurface(obj, 0, 0)
#     pt2 = rs.EvaluateSurface(obj, rs.SurfaceClosestPoint(obj, pt1))
#     vec = rs.CreateVector(0, 0, height)
#     pt3 = pt2 + vec
#     line = rs.AddLine(pt2, pt3)
#     if point2: rs.DeleteObjects(point2)
#     return line