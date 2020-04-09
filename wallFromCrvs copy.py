import rhinoscriptsyntax as rs
# !-RunPythonScript "wallsFromCrvs.py"

objs = rs.GetObjects("Pick curves to loft", rs.filter.curve, preselect=True)
width = rs.GetReal("width", 0.4)
height = rs.GetReal("height", 3)
plane = rs.ViewCPlane()

def offsetBothCrvs(crvs, width):
    if rs.IsCurveClosed(crvs):
        domain = rs.CurveDomain(crvs)
        parameter = (domain[0] + domain[1])/2.0
        rs.CurveSeam( crvs, parameter )
    offsets = [] 
    offsets.append(rs.OffsetCurve( crvs, [0,0,0], width/2))
    offsets.append(rs.OffsetCurve( crvs, [0,0,0], -width/2))
    section = rs.AddLoftSrf(offsets,loft_type=2)

    if offsets: rs.DeleteObjects(offsets)
    return section

def addRail(obj):
    point1 = rs.EvaluateSurface(obj, 0, 0)
    vec = rs.CreateVector(0, 0, height)
    point2 = rs.CopyObject(point1, vec)
    line = rs.AddLine(point1, point2)
    if point2: rs.DeleteObjects(point2)
    return line

def makeWall(crvs, width):
    rs.EnableRedraw(False)
    breps = []
    shapes = []

    for crv in crvs:
        rs.SimplifyCurve(crv)
        shape = offsetBothCrvs(crv, width)
        if rs.IsPolysurface(shape):
            surfs =rs.ExplodePolysurfaces(shape)
            for surf in surfs:
                shapes.append(surf)
            if shape: rs.DeleteObjects(shape)
        else:
            shapes.append(shape)
            

    for shape in shapes:
        railCurve = addRail(shape)
        breps.append(rs.ExtrudeSurface(shape, railCurve))
        if railCurve: rs.DeleteObjects(railCurve)

    if shapes: rs.DeleteObjects(shapes)
    rs.EnableRedraw(False)
    return breps

rs.SelectObjects(makeWall(objs, width))


        
# import rhinoscriptsyntax as rs
# # !-RunPythonScript "wallsFromCrvs.py"

# objs = rs.GetObjects("Pick curves to loft", rs.filter.curve, preselect=True)
# width = rs.GetReal("width", 0.4)
# height = rs.GetReal("height", 3)
# plane = rs.ViewCPlane()

# def wallBaseSrf(crv, width):
#     if rs.IsCurveClosed(crv):
#         domain = rs.CurveDomain(crv)
#         parameter = (domain[0] + domain[1])/2.0
#         rs.CurveSeam( crv, parameter )
#     offsets = map(lambda x: rs.OffsetCurve( crv, [0,0,0], x), [width/2, -width/2])
#     section = rs.AddLoftSrf(offsets,loft_type=2)

#     if offsets: rs.DeleteObjects(offsets)
#     return section


# def makeBrep(srf):
#     point1 = rs.EvaluateSurface(srf, 0, 0)
#     vec = rs.CreateVector(0, 0, height)
#     point2 = rs.CopyObject(point1, vec)
#     line = rs.AddLine(point1, point2)
#     brep = rs.ExtrudeSurface(srf, line)
#     if point2: rs.DeleteObjects(point2)
#     if line: rs.DeleteObjects(line)
#     retrun brep



# # def makeBrep(srf):
# #     rail = addRail(srf)
# #     brep = rs.ExtrudeSurface(srf, rail)
# #     if rail: rs.DeleteObjects(rail)
# #     return brep

# def makeWall(crv):
#     srfs = wallBaseSrf(crv, width)
#     breps = map(makeBrep, srfs)
#     if srfs: rs.DeleteObjects(srfs)
#     return wall

# rs.EnableRedraw(False)


# map(makeWall, objs)



# rs.EnableRedraw(True)


        
# # def addRail(obj):
# #     pt1 = rs.EvaluateSurface(obj, 0, 0)
# #     pt2 = rs.EvaluateSurface(obj, rs.SurfaceClosestPoint(obj, pt1))
# #     vec = rs.CreateVector(0, 0, height)
# #     pt3 = pt2 + vec
# #     line = rs.AddLine(pt2, pt3)
# #     if point2: rs.DeleteObjects(point2)
# #     return line