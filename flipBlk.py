import rhinoscriptsyntax as rs
import trkRhinoPy as trp

blockIds = rs.GetObjects("Pick Block", rs.filter.instance, preselect=True)

def checkblkplane(blkid):
    xform = rs.BlockInstanceXform(blkid)
    plane = rs.PlaneTransform(rs.WorldXYPlane(), xform)
    normal = plane.ZAxis.Z
    print normal
    if normal < 0:
        newxform = rs.XformMirror(plane.Origin, plane.Normal)
        return rs.TransformObject(blkid, newxform)
    else:
        return

map(checkblkplane, blockIds)