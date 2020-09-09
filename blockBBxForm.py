import rhinoscriptsyntax as rs

# walls = rs.GetObjects("Select solids", rs.filter.polysurface, preselect=True)
blks = rs.GetObjects("Select blocks", rs.filter.instance, preselect= True)

def bbsolid(obj):
    if rs.IsBlockInstance(obj):
        arrMatrix = rs.BlockInstanceXform(obj)
        if arrMatrix is not None:
            # pointId = rs.AddPoint([0,0,0])
            plane = rs.PlaneTransform(rs.WorldXYPlane(), arrMatrix)
            box = rs.BoundingBox(obj, plane)
            bb = rs.AddBox(box)
            plane.Origin = rs.SurfaceVolumeCentroid(bb)[0]
            # if box:
            #     for i, point in enumerate(box):
            #         rs.AddTextDot( i, point )
            xformscale = rs.XformScale((1.0,10.0,1.0))
            cob = rs.XformChangeBasis(rs.WorldXYPlane(), plane)
            cob_inverse = rs.XformChangeBasis(plane, rs.WorldXYPlane())
            temp = rs.XformMultiply(xformscale, cob)
            xform = rs.XformMultiply(cob_inverse, temp)
            rs.TransformObjects(bb, xform)
            return bb

if blks:
    rs.EnableRedraw(False)
    solids = [bbsolid(blk) for blk in blks]
    if solids:
        groupname = rs.AddGroup()
        rs.AddObjectsToGroup(solids, groupname)
        rs.UnselectAllObjects()
        rs.SelectObjects(solids)
    rs.EnableRedraw(True)

# print solids
# print walls