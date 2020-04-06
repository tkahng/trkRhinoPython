import rhinoscriptsyntax as rs

obj = rs.GetObject("Select a srf", rs.filter.surface)
# obj = rs.GetObject("Select object", rs.filter.surface + rs.filter.polysurface)

intervalx = rs.GetReal("intervalx", 1)
intervaly = rs.GetReal("intervaly", 2)
Secx = rs.GetReal("mullion width", 0.15) 
Secy = rs.GetReal("mullion depth", 0.05) 
louverW = rs.GetReal("louverW width", 0.5) 

vec1 = (-Secx/2, -Secy, 0)
vec2 = (-Secx/2, -Secy/2, 0)
vec3 = (-louverW/2, -louverW/2, 0)

def profile2(plane, vec):
    rs.ViewCPlane(None, plane)
    sec = rs.AddLine((0,0,0), (louverW,0,0))
    sec = rs.RotateObject(sec, plane.Origin, 45.0, plane.ZAxis, copy=True)

    # if sec: rs.DeleteObjects(sec)
    return sec

def sweepSec(crv, plane, vec):
    # rs.AddPlaneSurface( plane, 1, 1 )
    rect = profile2(plane, vec)
    sweep = rs.AddSweep1(crv, rect, closed=True)
    sweep = rs.CapPlanarHoles(sweep)
    if rect: rs.DeleteObjects(rect)
    if crv: rs.DeleteObjects(crv)
    return sweep

def flipBool(tf):
    return abs(tf-1)

def intervals(srf, uv, spacing):
    domains = []
    domain = rs.SurfaceDomain(srf, uv)
    i = spacing
    while i < domain[1]:
        domains.append(i)
        i = i+spacing
    return domains

def intervalpts(srf, uv, spacing):

    spacings = intervals(srf, uv, spacing)
    ptlist = []
    
    for i in spacings:
        coord = []
        coord.append(i)
        coord.insert(flipBool(uv), 0)
        ptlist.append(coord)   

    return ptlist

def isoframe(srf, uv, spacing, vec):

    points = intervalpts(srf, uv, spacing)
    print points
    sweeps = []
    
    for i in points:
        point = rs.EvaluateSurface(srf, i[0], i[1])
        parameter = rs.SurfaceClosestPoint(srf, point)
        plane = rs.SurfaceFrame(srf, parameter)
        crv = rs.ExtractIsoCurve( srf, parameter, flipBool(uv))
        direction = rs.CurveTangent(crv, 0)
        newplane = rs.PlaneFromNormal(point, direction, plane.ZAxis)
        sweeps.append(sweepSec(crv, newplane, vec))

    return sweeps    



def framelouver(srf):
    frames = []
    frames.append(isoframe(srf, 0, intervalx, vec3))
    return frames
    

framelouver(obj)
