import rhinoscriptsyntax as rs
import scriptcontext as sc
import trkRhinoPy as trp
# import Rhino as rc

# sc.doc = rc.RhinoDoc.ActiveDoc
objs = rs.GetObjects("Select polysurface to explode", rs.filter.polysurface|rs.filter.mesh|rs.filter.instance, preselect=True)

def blkPlane(obj):
    xform = rs.BlockInstanceXform(obj)
    plane = rs.PlaneTransform(rs.WorldXYPlane(), xform)
    return plane

def srfPlane(obj):
    tempplane = trp.getSrfFrame(obj)
    plane = rs.CreatePlane(tempplane.Origin, rs.VectorCrossProduct(tempplane.ZAxis, rs.WorldXYPlane().ZAxis), tempplane.ZAxis)
    return plane

def blkFace(obj):

    cameraPos = rs.ViewCamera()

    cameraPos.Z = 0
    
    plane = rs.WorldXYPlane()

    if rs.IsBlockInstance(obj):
        plane = blkPlane(obj)
    elif rs.IsSurface(obj):
        plane = srfPlane(obj)

    targetpos = plane.Origin
    targetpos.Z = 0

    viewdir = rs.VectorUnitize(cameraPos - targetpos)

    angle = rs.VectorAngle(viewdir, plane.YAxis)

    newXform = rs.XformRotation3(plane.YAxis, viewdir, plane.Origin)

    rs.TransformObject(obj, newXform)

map(blkFace, objs)


