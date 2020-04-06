import rhinoscriptsyntax as rs

crvIds = rs.GetObjects("Pick curves", rs.filter.curve)
ptIds = rs.GetObjects("Pick points", rs.filter.point)
blockId = rs.GetObject("Pick Block", rs.filter.instance)

if rs.IsBlockInstance(blockId):
    block_name = rs.BlockInstanceName(blockId)

for crv in crvIds:
    for pt in ptIds:
        if rs.IsPointOnCurve(crv, pt):
            param = rs.CurveClosestPoint(crv, pt)
            tangent = rs.CurveTangent(crv, param)
            tangent = rs.VectorUnitize(tangent)
            normal = rs.WorldXYPlane().ZAxis
            # normal = rs.VectorUnitize(normal)
            plane = rs.PlaneFromNormal(pt, normal, tangent)
            # plane = rs.CurvePerpFrame(crv, param)
            xform = rs.XformChangeBasis(plane, rs.WorldXYPlane())
            rs.InsertBlock2(block_name, xform)
