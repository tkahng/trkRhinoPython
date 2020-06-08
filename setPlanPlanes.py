import rhinoscriptsyntax as rs
import trkRhinoPy as trp
import scriptcontext as sc
import json

count = rs.GetInteger("number of planes")
origin = rs.GetPoint("pick origin")
startPt = rs.GetPoint("pick start")

vec = startPt - origin

planplanes = []

for i in range(count):
    lvlname = i+1
    newvec = vec * i
    newpt = startPt + newvec
    rs.AddPoint(newpt)
    ptdict = dict({"point":{"Z":newpt.Z, "Y":newpt.Y, "X":newpt.X}, "level":lvlname})
    planplanes.append(ptdict)
    # print ptdict
    # newplane = rs.PlaneFromNormal(newpt, (0,0,1))
    # vecs.append(newplane)

sc.sticky["planplanes2"] = json.dumps(planplanes)
rs.SetDocumentUserText("planplanes", json.dumps(planplanes))

# a = vecs
# vector = direction

# def rMove(vector):
#     if objs != None:
#         rs.MoveObjects( objs, vector)
#         objs = None
#         vector = vector + inputvec
#         rMove(vector)
# pts = []



# def arrayPt(point, vec, count):
#     vec = x
#     count = y

#     vecs = []

#     for i in range(count):
#         newvec = vec * i
#         vecs.append(newvec)

#     a = vecs

# arrayPt(origin, direction, planCount)

        

# vector = direction
# pt = origin
# def arrayPt(vector):
#     for i in range(count):
#         pt = pt + direction
#         pts.append(pt)

# def arrayPt(pt, vec, count):
#     for i in range(count):





# # direction = 

# import rhinoscriptsyntax as rs
# import Rhino.Geometry as rg


# vec = x
# count = y
# startpt = z
# vecs = []

# #for idx, i in enumerate(range(count), start=1):
# #    lvlname = idx
# #    newvec = vec * idx
# #    print newvec
# #    newpt = startpt + newvec
# #    print newpt
# #    ptdict = dict(level=lvlname, point = [newpt.X, newpt.Y, newpt.Z])
# #    print ptdict
# #    newplane = rs.PlaneFromNormal(newpt, (0,0,1))
# #    vecs.append(newplane)

# for i in range(count):
#     lvlname = i+1
#     newvec = vec * i
#     print newvec
#     newpt = startpt + newvec
#     print newpt
#     ptdict = dict({"level":lvlname, "point":{"X":newpt.X, "y":newpt.Y, "z":newpt.Z}})
#     print ptdict
#     newplane = rs.PlaneFromNormal(newpt, (0,0,1))
#     vecs.append(newplane)

# a = vecs