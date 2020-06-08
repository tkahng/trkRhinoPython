import rhinoscriptsyntax as rs
# !-RunPythonScript "objectBottomFaceArea.py"

# rs.EnableRedraw(False)
faces = []
bndry = []
obj = rs.GetObject("Select polysurface to explode", rs.filter.polysurface, preselect=True)
if rs.IsPolysurface(obj):
    faces = rs.ExplodePolysurfaces( obj )

for face in faces:
    if rs.IsSurface(face):
        domainU = rs.SurfaceDomain(face, 0)
        domainV = rs.SurfaceDomain(face, 1)
        u = domainU[1]/2.0
        v = domainV[1]/2.0
        point = rs.EvaluateSurface(face, u, v)
        param = rs.SurfaceClosestPoint(face, point)
        normal = rs.SurfaceNormal(face, param)
        # print normal
        if normal.Z == -1:
            bndry.append(face)

for bnd in bndry:
    area = rs.SurfaceArea(bnd)[0]
    areapy = area/3.3058
    print area, areapy
    txt = rs.ClipboardText(area)

if faces: rs.DeleteObjects(faces)

def calcArea(srfs):
    areas = []
    for srf in srfs:
        areas.append(rs.SurfaceArea(srf)[0])
    totalArea = sum(areas)
    totalAreaPy = totalArea/3.3058
    print area, areapy
    txt = rs.ClipboardText(area)


