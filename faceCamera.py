import rhinoscriptsyntax as rs
import scriptcontext as sc
# import Rhino as rc

# sc.doc = rc.RhinoDoc.ActiveDoc
objs = rs.GetObjects("Select polysurface to explode", rs.filter.polysurface|rs.filter.mesh|rs.filter.instance, preselect=True)


def blkFace(obj):

    cameraPos = rs.ViewCamera()

    cameraPos.Z = 0

    xform = rs.BlockInstanceXform(obj)
    plane = rs.PlaneTransform(rs.WorldXYPlane(), xform)

    viewdir = rs.VectorUnitize(cameraPos - plane.Origin)

    angle = rs.VectorAngle(viewdir, plane.YAxis)

    newXform = rs.XformRotation3(plane.YAxis, viewdir, plane.Origin)

    # newplane = rs.RotatePlane(plane, angle, plane.ZAxis)

    # newXform = rs.XformChangeBasis(plane, newplane)

    rs.TransformObject(obj, newXform)

map(blkFace, objs)


