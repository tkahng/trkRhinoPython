# -*- coding: utf-8 -*-
import rhinoscriptsyntax as rs 
import scriptcontext as sc
import json
import ast

def intFlipBool(tf):
    return abs(tf-1)

'''QuickTag'''

def setQuickTag(obj, tagVal):
    rs.SetUserText(obj, 'tag', tagVal)

def getQuickTag(tagVal):
    rs.Command('_SelKeyValue tag {}'.format(tagVal))

def objsSetQuickTag():
    objs = rs.GetObjects('select objects to tag', preselect=True)
    tagVal = rs.GetString('Tag Value')
    map(lambda x: setQuickTag(x, tagVal), objs)

def objsGetQuickTag():
    tagVal = rs.GetString('Tag Value')
    rs.Command('_SelKeyValue tag {}'.format(tagVal))

'''object user text utils'''

def setSourceLayer(obj, source):
    sourceLayer = rs.ObjectLayer(source)
    rs.SetUserText(obj, 'source Layer', sourceLayer)

def copySourceLayer(obj, source):
    sourceLayer = rs.ObjectLayer(source)
    rs.ObjectLayer(obj, sourceLayer)

def getSourceKeys(source):
    if rs.IsUserText(source) == 0:
        print 'no keys'
        return
    return [ x for x in rs.GetUserText(source) if "BakeName" not in x ]
    # return [ x for x in rs.GetUserText(source)]

def sourceKeyValue(source):
    keys = getSourceKeys(source)
    values = map(lambda x: rs.GetUserText(source, x), keys)
    return keys, values

def copySourceData(obj, source):
    if rs.IsUserText(source) == 0:
        return
    keyValue = sourceKeyValue(source)
    # print keyValue
    map(lambda x, y: rs.SetUserText(obj, x, y), keyValue[0], keyValue[1])

def valuesFromLayer(obj):
    """get values from layer name
    
    Arguments:
        obj {obj} -- any object with a attribute descriptive layer name
    
    Returns:
        list -- list of values
    """    
    layer = rs.ObjectLayer(obj)
    if "::" in layer:
        layer = layer.split("::")
        layer = layer[-1]
    if " " in layer:
        values = layer.split(" ")
        return values
    else:
        return [layer]

def hatchFromSrf(srf):
    border = rs.DuplicateSurfaceBorder(srf, type=0)
    hatch = rs.AddHatches(border, "SOLID")
    rs.DeleteObjects(border)
    return hatch    

def setValueByLayer(obj, keys):
    keys = keys.split()
    values = valuesFromLayer(obj)
#    values[1], values[-1] = values[-1], values[1]
    kv = zip(keys, values)
    map(lambda x: rs.SetUserText(obj, x[0], x[1]), kv)

def setSrfAreaValue(obj):
    area = calcArea(obj)
    rs.SetUserText(obj, "area", str(area[0]))
    rs.SetUserText(obj, "areapy", str(area[1]))
    return area[0]

def setBrepFA(obj):
    faces = getBottomFace(obj)
    area = calcAreas(faces)
    rs.SetUserText(obj, "area", str(area[0]))
    rs.SetUserText(obj, "areapy", str(area[1]))
    rs.DeleteObjects(faces)

def setObjAreaValue(obj):
    if rs.IsSurface(obj):
        setSrfAreaValue(obj)
    elif rs.IsPolysurface(obj) and rs.IsPolysurfaceClosed(obj):
        setBrepFA(obj)
    else:
        rs.SetUserText(obj, "area", 'na')

def setBrepHeight(obj):
    if rs.IsPolysurface(obj) and rs.IsPolysurfaceClosed(obj):
        height = brepGetZ(obj)
        height = height[2]
        rs.SetUserText(obj, "height", str(height))

def boolToggle(input):
    if len(input) == 0:
        return False
    else:
        return True

"""Geo Utils """

def castToM(islen, value):
    factor = 0.001
    if not islen:
        factor = factor*factor
    docUnits = rs.UnitSystem()
    if docUnits == 2:
        return value * factor
    else:
        return value

# def castMToUnit(value):
#     factor = 0.001
#     docUnits = rs.UnitSystem()
#     if docUnits == 2:
#         return value * factor
#     else:
#         return value

def calcArea(srf):
    area = rs.SurfaceArea(srf)[0]
    totalArea = round(castToM(False, area), 2)
    totalAreaPy = round(totalArea/3.3058, 2)
    return [totalArea, totalAreaPy]
    # txt = rs.ClipboardText(totalArea)

def calcAreas(srfs):
    areas = []
    for srf in srfs:
        areas.append(rs.SurfaceArea(srf)[0])
    # totalArea = round(castToM(False, sum(areas)), 2)
    # totalAreaPy = round(totalArea/3.3058, 2)
    totalArea = castToM(False, sum(areas))
    totalAreaPy = totalArea/3.3058
    return [round(totalArea, 2), round(totalAreaPy, 2)]
    # txt = rs.ClipboardText(totalArea)

def rebuildSrfCrv(obj):
    crv = rs.DuplicateSurfaceBorder(obj, type=0)
    map(lambda x: rs.SimplifyCurve(x), crv)
    return crv

def rebuildBrep(obj):
    srfs = rs.ExplodePolysurfaces(obj)
    crvs = map(rebuildSrfCrv, srfs)
    rs.DeleteObjects(srfs)
    newSrfs = map(rs.AddPlanarSrf, crvs)
    # newSrfs = rs.AddPlanarSrf(crvs)
    rs.DeleteObjects(crvs)
    newbrep = rs.JoinSurfaces(newSrfs, delete_input=True)
    try:
        copySourceLayer(newbrep, obj)
        copySourceData(newbrep, obj)
    except:
        pass
    rs.DeleteObject(obj)
    # return newbrep

def getBottomFace(obj):
    faces = rs.ExplodePolysurfaces(obj)
    output = []
    [output.append(face) if getSrfNormal(face).Z == -1 else rs.DeleteObject(face) for face in faces]
    return output

def getSrfNormal(srf):
    domainU = rs.SurfaceDomain(srf, 0)
    domainV = rs.SurfaceDomain(srf, 1)
    u = domainU[1]/2.0
    v = domainV[1]/2.0
    point = rs.EvaluateSurface(srf, u, v)
    param = rs.SurfaceClosestPoint(srf, point)
    return rs.SurfaceNormal(srf, param)

def getSrfFrame(srf):
    domainU = rs.SurfaceDomain(srf, 0)
    domainV = rs.SurfaceDomain(srf, 1)
    u = domainU[1]/2.0
    v = domainV[1]/2.0
    point = rs.EvaluateSurface(srf, u, v)
    param = rs.SurfaceClosestPoint(srf, point)
    return rs.SurfaceFrame(srf, param)

def offsetInside(crv, dist):
    rs.SimplifyCurve(crv)
    centroid = rs.CurveAreaCentroid(crv)
    return rs.OffsetCurve(crv, centroid[0], dist)

def brepGetZ(obj):
    box = rs.BoundingBox(obj)
    minZ = box[0].Z
    maxZ = box[-1].Z
    height = maxZ - minZ
    return minZ, maxZ, round(height, 3)

def objBBPts(obj):
    box = rs.BoundingBox(obj)
    minZ = box[0]
    maxZ = box[-2]
    mid = (box[0] + box[-2])/2
    return minZ, maxZ, mid
    # rs.addpoint

def moveSrftoZ(srf):
    domainU = rs.SurfaceDomain(srf, 0)
    domainV = rs.SurfaceDomain(srf, 1)
    u = domainU[1]/2.0
    v = domainV[1]/2.0
    point = rs.EvaluateSurface(srf, u, v)
    # vec = [0, 0, point.Z]
    # vec = rs.VectorReverse(vec)
    # vec = [0,0,vec.Z]
    rs.MoveObjects(srf, rs.VectorReverse([0, 0, point.Z]))

"""Level Tools"""

def brepPtZPair(brep):
    el = round(brepGetZ(brep)[0], 3)
    return [brep, el]

def srfPtZPair(srf):
    domainU = rs.SurfaceDomain(srf, 0)
    domainV = rs.SurfaceDomain(srf, 1)
    u = domainU[1]/2.0
    v = domainV[1]/2.0
    point = rs.EvaluateSurface(srf, u, v)
    el = round(point.Z, 3)
    return [srf, el]

def crvPtZpair(crv):
    el = round(brepGetZ(crv)[0], 3)
    return [crv, el]

# def crvPtZpair(crv):
#     domain = rs.CurveDomain(crv)
#     t = domain[1]/2.0
#     point = rs.EvaluateCurve(crv, t)
#     el = round(point.Z, 3)
#     return [crv, el]

def setObjZPair(obj):
    if rs.IsCurve(obj):
        return crvPtZpair(obj)
    elif rs.IsPolysurfaceClosed(obj):
        return brepPtZPair(obj)
    elif rs.IsSurface(obj):
        return srfPtZPair(obj)
    elif rs.IsPoint(obj):
        pt = rs.CreatePoint(obj)
        return [obj, round(pt.Z, 3)]
    else:
        pass

def groupByElevation(objs, isUG):
    pairs = map(setObjZPair, objs)
    values = set(map(lambda x:x[1], pairs))
    newpairs = [[y for y in pairs if y[1]==x] for x in values]
    return sorted(newpairs, key=lambda x:x[0][1], reverse=isUG)

def setLevel(sortedpairs, isUG, func):
    for idx, pairs in enumerate(sortedpairs, start=1):
        grade = 'ag'
        if isUG: 
            idx = -idx
            grade = 'ug'
        map(lambda x: func(x, idx, grade), pairs)

def setDictforDatum(x, idx, grade):
    keys = 'level grade elevation'
    keys = keys.split()
    vals = [idx, grade, str(x[1])]
    lvldict = dict(zip(keys, vals))
    rs.SetUserText(x[0], 'lvldict', lvldict)

def setLevelforObj(x, idx, grade):
    rs.SetUserText(x[0], "level", str(idx))
    rs.SetUserText(x[0], "grade", grade)
    rs.SetUserText(x[0], "elevation", str(x[1]))    

def setLevelforDatum(x, idx, grade):
    rs.SetUserText(x[0], "level", str(idx))
    rs.SetUserText(x[0], "grade", grade) 
    rs.SetUserText(x[0], "elevation", str(x[1]))
    # rs.SetUserText(x[0], 'pt', )
    setBrepHeight(x[0])

def cPlaneLvl():
    userstr = rs.GetDocumentUserText("levels")
    objdict = ast.literal_eval(userstr)
    for i in objdict:
        lvlname = i["level"]
        elevation = float(i["elevation"])
        newplane = rs.CreatePlane((0,0,elevation))
        rs.ViewCPlane(None, newplane)
        rs.AddNamedCPlane(lvlname)

def createSectionBox(obj):
    box = rs.BoundingBox(obj)
    bb = rs.AddBox(box)
    faces = rs.ExplodePolysurfaces(bb)
    faces = [rs.FlipSurface(x) for x in faces]
    planes = [getSrfFrame(x) for x in faces]
    clips = [rs.AddClippingPlane(x, 1000, 1000) for x in planes]
    group = rs.AddGroup()
    rs.AddObjectsToGroup(clips, group)
    return clips



"""Dictionary Json"""

def createObjDict(obj):
    # objkeys = [ x for x in rs.GetUserText(obj) if "BakeName" not in x ]
    objkeys = [ x for x in rs.GetUserText(obj)]
    objvals = map(lambda x: rs.GetUserText(obj, x), objkeys)
    return dict(zip(objkeys, objvals))

    

"""Block Tools"""

def redefineBlockScale(block):
    block_name = rs.BlockInstanceName(block)
    # rs.RenameBlock (block_name, "{}-old".format(block_name))
    blockXform = rs.BlockInstanceXform(block)
    plane = rs.PlaneTransform(rs.WorldXYPlane(), blockXform)
    cob = rs.XformChangeBasis(plane, rs.WorldXYPlane())
    cob_inverse = rs.XformChangeBasis(rs.WorldXYPlane(), plane)
    refBlock = rs.TransformObjects(block, cob_inverse, True )
    exploded = rs.ExplodeBlockInstance(refBlock)
    rs.AddBlock(exploded, rs.WorldXYPlane().Origin, block_name, True)
    newBlock = rs.InsertBlock2(block_name, cob)
    copySourceLayer(newBlock, block)
    try:
        copySourceData(newBlock, block)
    except:
        pass
    rs.DeleteObjects(block)

def resetBlockScale(block):
    block_name = rs.BlockInstanceName(block)
    blockXform = rs.BlockInstanceXform(block)
    plane = rs.PlaneTransform(rs.WorldXYPlane(), blockXform)
    # newplane = rs.CreatePlane(plane.Origin, plane.XAxis, plane.YAxis)
    # cob = rs.XformChangeBasis(newplane, rs.WorldXYPlane())
    cob = rs.XformChangeBasis(plane, rs.WorldXYPlane())
    newBlock = rs.InsertBlock2(block_name, cob)
    copySourceLayer(newBlock, block)
    try:
        copySourceData(newBlock, block)
    except:
        pass
    rs.DeleteObjects(block)
    return newBlock

def blkFace(obj):

    cameraPos = rs.ViewCamera()

    cameraPos.Z = 0

    xform = rs.BlockInstanceXform(obj)
    plane = rs.PlaneTransform(rs.WorldXYPlane(), xform)

    viewdir = rs.VectorUnitize(cameraPos - plane.Origin)

    angle = rs.VectorAngle(viewdir, plane.YAxis)

    newXform = rs.XformRotation3(plane.YAxis, viewdir, plane.Origin)

    rs.TransformObject(obj, newXform)