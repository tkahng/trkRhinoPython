import rhinoscriptsyntax  as rs
import scriptcontext as sc
import Rhino


def ReplaceObject():
    
    """
    Have the user orient 1 replacement correctly to one target.
    
    get a plane from frame on brep face[0]
    Get plane-plane transform from target to a plane on the same face on the other targets
    
    See if it works for meshes - just pick any face and do the same thing - get the plane from the
    face verts.
    
    """
    
    targId = rs.GetObject("Select the first object to replace",  filter=8+16)
    if not targId:return
    
    obj = sc.doc.Objects.Find(targId)
    geo = obj.Geometry
    
    extrusion = False
    if isinstance(geo, Rhino.Geometry.Extrusion):
        extrusion = True
        geo = geo.ToBrep()
    
    face = geo.Faces[0]
    faceCount = geo.Faces.Count
    faceBrep = face.DuplicateFace(False)
    area = faceBrep.GetArea()
    
    srf = face.UnderlyingSurface()
    rc, plane = srf.FrameAt(srf.Domain(0).Mid, srf.Domain(1).Mid)
    if not rc:
        print "Error finding base plane."
        return
        
    ids = rs.GetObjects("Now select the other objects to replace.")
    if not ids:return
    
    newIds = rs.GetObjects("Select replacement objects")
    if not newIds: return
    
    tol = sc.doc.ModelAbsoluteTolerance
    
    rs.EnableRedraw(False)
    
    for ID in ids:
        
        tempGeo = sc.doc.Objects.Find(ID).Geometry

        if isinstance(tempGeo, Rhino.Geometry.Extrusion):
            tempGeo = tempGeo.ToBrep()
            
        tempFace = tempGeo.Faces[0]
        tempFaceBrep = tempFace.DuplicateFace(False)

        if abs(tempFaceBrep.GetArea() - area) > tol*10 or tempGeo.Faces.Count != faceCount:
            continue
        
        tempSrf = tempFace.UnderlyingSurface()
        rc, tempPlane = tempSrf.FrameAt(tempSrf.Domain(0).Mid, tempSrf.Domain(1).Mid)
        
        xForm = Rhino.Geometry.Transform.PlaneToPlane(plane, tempPlane)
        
        for newId in newIds:
            rs.TransformObject(newId, xForm, True)
        rs.DeleteObject(ID)
        
    rs.DeleteObject(targId)
    
    rs.EnableRedraw(True)
    
    
if __name__ == '__main__':ReplaceObject()