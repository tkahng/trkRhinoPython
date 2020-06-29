import rhinoscriptsyntax as rs
import trkRhinoPy as trp

objs = rs.GetObjects("Select polysurface to explode", rs.filter.polysurface|rs.filter.mesh|rs.filter.instance, preselect=True)

cameraPos = rs.ViewCamera()


def faceSrf(obj):
    srfDir = trp.getSrfNormal(obj)

def faceBlk(obj):
    sourceXform = rs.BlockInstanceXform(source)
