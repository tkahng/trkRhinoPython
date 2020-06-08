# !-RunPythonScript "framesrf.py"
# Surface must be Reparametrized with Auto option
import rhinoscriptsyntax as rs
import trkRhinoPy as trp

objs = rs.GetObjects("Select a srf", rs.filter.surface, preselect=True)
eq = rs.GetString('eq?')
eq = not trp.boolToggle(eq)

option = rs.GetInteger('option', number=3)

if option == 2:
    intervalx = rs.GetReal("intervalx", 0.5)
else:
    intervalx = rs.GetReal("intervalx", 1)
    intervaly = rs.GetReal("intervaly", 2)
Secx = rs.GetReal("mullion width", 0.15) 
Secy = rs.GetReal("mullion depth", 0.05) 

vec1 = (-Secx/2, -Secy, 0)
vec2 = (-Secx/2, -Secy/2, 0)

def rectFrame():
    return rs.AddRectangle(rs.WorldXYPlane(), Secx, Secy )

def profileXform(sec, plane, vec):
    xvec = rs.XformTranslation(vec)
    cob = rs.XformChangeBasis(plane, rs.WorldXYPlane())
    xform = rs.XformMultiply(cob, xvec)
    return rs.TransformObjects(sec, xform, False)

def sweepSec(crv, plane, vec):
    rect = profileXform(rectFrame(), plane, vec)
    sweep = rs.AddSweep1(crv, rect, closed=True)
    # sweep = rs.CapPlanarHoles(sweep)
    rs.CapPlanarHoles(sweep)
    if rect: rs.DeleteObjects(rect)
    if crv: rs.DeleteObjects(crv)
    return sweep[0]

def intFlipBool(tf):
    return abs(tf-1)

def Intervals(srf, uv, spacing, eq):
    domains = []
    domain = rs.SurfaceDomain(srf, uv)
    if eq:
        count = int(round(domain[1]/spacing))
        dist = domain[1]/count
    else:
        dist = spacing
    i = dist
    while i < domain[1]:
        domains.append(i)
        i = i+dist
    return domains

def intervalEnds(srf, uv, spacing):
    spacings = Intervals(srf, uv, spacing, eq)
    ptlist = []
    for i in spacings:
        coord = []
        coord.append(i)
        coord.insert(intFlipBool(uv), 0)
        ptlist.append(coord)   
    return ptlist


def intervalpts(srf, uv, spacing):
    spacings = Intervals(srf, uv, spacing, eq)
    ptlist = []
    for i in spacings:
        coord = []
        coord.append(i)
        coord.insert(intFlipBool(uv), 0)
        ptlist.append(coord)   
    return ptlist

def isoframe(srf, uv, spacing, vec):
    points = intervalpts(srf, uv, spacing)
    sweeps = []
    for i in points:
        point = rs.EvaluateSurface(srf, i[0], i[1])
        parameter = rs.SurfaceClosestPoint(srf, point)
        plane = rs.SurfaceFrame(srf, parameter)
        crv = rs.ExtractIsoCurve(srf, parameter, intFlipBool(uv))
        direction = rs.CurveTangent(crv, 0)
        newplane = rs.PlaneFromNormal(point, direction, plane.ZAxis)
        sweeps.append(sweepSec(crv, newplane, vec))
    return sweeps   

def extframe2(srf, uv, spacing, vec):
    points = intervalpts(srf, uv, spacing)
    sweeps = []
    for i in points:
        point = rs.EvaluateSurface(srf, i[0], i[1])
        parameter = rs.SurfaceClosestPoint(srf, point)
        plane = rs.SurfaceFrame(srf, parameter)
        crv = rs.ExtractIsoCurve(srf, parameter, intFlipBool(uv))
        direction = rs.CurveTangent(crv, 0)
        newplane = rs.PlaneFromNormal(point, direction, plane.ZAxis)
        sweeps.append(sweepSec(crv, newplane, vec))
    return sweeps   

# def railSweep(srf, crv, vec):
#     point = rs.CurveStartPoint(crv)
#     parameter = rs.SurfaceClosestPoint(srf, point)
#     plane = rs.SurfaceFrame(srf, parameter)
#     direction = rs.CurveTangent(crv, 0)
#     newplane = rs.PlaneFromNormal(point, direction, plane.ZAxis)
#     frame = sweepSec(crv, newplane, vec)
#     if crv: rs.DeleteObjects(crv)
#     return frame

# def extframe(srf, vec):
#     # frames = []
#     crv = rs.DuplicateSurfaceBorder(srf, type=1)
#     rs.SimplifyCurve(crv)
#     if rs.IsPolyCurve(crv):
#         crvs = rs.ExplodeCurves(crv)
#     elif rs.IsPolyline(crv):
#         crvs = [crv]
#     frames = map(lambda x: railSweep(srf, x, vec), crvs)
#     return frames
def extframe(srf, vec):
    frames = []
    crv = rs.DuplicateSurfaceBorder(srf, type=1)
    rs.SimplifyCurve(crv)

    domain = rs.CurveDomain(crv)
    param = (domain[0] + domain[1])/2.0
    rs.CurveSeam(crv, param)

    point = rs.EvaluateCurve(crv, 0)
    parameter = rs.SurfaceClosestPoint(srf, point)
    plane = rs.SurfaceFrame(srf, parameter)
    direction = rs.CurveTangent(crv, 0)
    newplane = rs.PlaneFromNormal(point, direction, plane.ZAxis)
    frame.append(sweepSec(crv, newplane, vec))
    if crv: rs.DeleteObjects(crv)
    return frames

def frameFunc(srf, x, y, v1, v2):
    vFrames = isoframe(srf, 0, x, v2)
    hFrames = isoframe(srf, 1, x, v2)
    xFrames = extframe(srf, v1)


def framemulti(srfs):
    rs.EnableRedraw(False)
    rs.SelectObjects(srfs)
    rs.Command("reparameterize a")
    rs.UnselectAllObjects()
    frames = []
    allgroup = rs.AddGroup()
    for srf in srfs:
        group = rs.AddGroup()
        frame = []
        if option == 2: 
            frame.append(isoframe(srf, 0, intervalx, vec2))
        elif option == 1:
            frame.append(isoframe(srf, 0, intervalx, vec2))
            frame.append(extframe(srf))
        else:
            frame.append(isoframe(srf, 0, intervalx, vec2))
            frame.append(isoframe(srf, 1, intervaly, vec2))
            frame.append(extframe(srf, vec1))
        frame = [x for x in frame if x]
        frame = list(reduce(lambda x, y: x+y, frame))
        rs.AddObjectsToGroup(frame,group)
        frames.append(frame)
        # print frame
    # for frame in frames: rs.SelectObjects(frame)
    frames = [x for x in frames if x]
    frames = list(reduce(lambda x, y: x+y, frames))
    rs.AddObjectsToGroup(frames,allgroup)
    rs.SelectObjects(frames)
    rs.EnableRedraw(True)
    return frames
    
if __name__ == '__main__':
    framemulti(objs)