import rhinoscriptsyntax as rs

# walls = rs.GetObjects("Select solids", rs.filter.polysurface, preselect=True)
blks = rs.GetObjects("Select blocks", rs.filter.instance)

proxyBlk = rs.GetObject("Select block", rs.filter.instance)


# def bbsolid(obj):
#     if rs.IsBlockInstance(obj):
#         arrMatrix = rs.BlockInstanceXform(obj)
#         if arrMatrix is not None:
#             pointId = rs.AddPoint([0,0,0])
#             plane = rs.PlaneTransform(rs.WorldXYPlane(), arrMatrix)
#             box = rs.BoundingBox(obj, plane)
#             bb = rs.AddBox(box)
#             # if box:
#             #     for i, point in enumerate(box):
#             #         rs.AddTextDot( i, point )
#             xformscale = rs.XformScale((1.0,20.0,1.0))
#             cob = rs.XformChangeBasis(rs.WorldXYPlane(), plane)
#             cob_inverse = rs.XformChangeBasis(plane, rs.WorldXYPlane())
#             temp = rs.XformMultiply(xformscale, cob)
#             xform = rs.XformMultiply(cob_inverse, temp)
#             rs.TransformObjects(bb, xform)
#             return bb

def applyXform(target, source):
    targetXform = rs.BlockInstanceXform(target)
    sourceXform = rs.BlockInstanceXform(source)
    if targetXform is not None:
        plane = rs.PlaneTransform(rs.WorldXYPlane(), targetXform)
        # xformscale = rs.XformScale((1.0,20.0,1.0))
        cob = rs.XformChangeBasis(rs.WorldXYPlane(), plane)
        cob_inverse = rs.XformChangeBasis(plane, rs.WorldXYPlane())
        temp = rs.XformMultiply(sourceXform, cob)
        xform = rs.XformMultiply(cob_inverse, temp)
        rs.TransformObjects(target, xform)

    

if blks:
    rs.EnableRedraw(False)
    [applyXform(blk, proxyBlk) for blk in blks]
    rs.EnableRedraw(True)

# if blks:
#     rs.EnableRedraw(False)
#     solids = [bbsolid(blk) for blk in blks]
#     if solids:
#         groupname = rs.AddGroup()
#         rs.AddObjectsToGroup(solids, groupname)
#         rs.SelectObjects(solids)
#     rs.EnableRedraw(True)