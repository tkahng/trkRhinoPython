import rhinoscriptsyntax as rs

objs = rs.GetObjects('select objs', rs.filter.surface|rs.filter.curve|rs.filter.point, preselect=True)
grade = rs.GetString("toggle grade")

def boolToggle(grade):
    if len(grade) == 0:
        return False
    else:
        return True

def srfPtZPair(srf):
    domainU = rs.SurfaceDomain(srf, 0)
    domainV = rs.SurfaceDomain(srf, 1)
    u = domainU[1]/2.0
    v = domainV[1]/2.0
    point = rs.EvaluateSurface(srf, u, v)
    el = round(point.Z, 3)
    return [srf, el]

def crvPtZpair(crv):
    domain = rs.CurveDomain(crv)
    t = domain[1]/2.0
    point = rs.EvaluateCurve(crv, t)
    el = round(point.Z, 3)
    return [crv, el]



def setObjZPair(obj):
    if rs.IsCurve(obj):
        return crvPtZpair(obj)
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

def setLevel(sortedpairs, isUG):
    for idx, pairs in enumerate(sortedpairs, start=1):
        grade = 'ag'
        if isUG: 
            idx = -idx
            grade = 'ug'
        map(lambda x: setDictforDatum(x, idx, grade), pairs)

def setDictforDatum(x, idx, grade):
    keys = 'level grade elevation'
    keys = keys.split()
    vals = [idx, grade, str(x[1])]
    lvldict = dict(zip(keys, vals))
    rs.SetUserText(x[0], 'lvldict', lvldict)

def setLevelforObj(x, idx, grade):
    rs.SetUserText(x[0], "level", str(idx))
    rs.SetUserText(x[0], "grade", grade)    

def setLevelforDatum(x, idx, grade):
    rs.SetUserText(x[0], "level", str(idx))
    rs.SetUserText(x[0], "grade", grade) 
    rs.SetUserText(x[0], "elevation", str(x[1]))       



def process(objs, grade):
    isUG = boolToggle(grade)
    groups = groupByElevation(objs, isUG)
    setLevel(groups, isUG)

if __name__ == '__main__':
    process(objs, grade)  # Put the a call to the main function in the file.    