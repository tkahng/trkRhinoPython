import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino

def AddToBlock():
    objects = rs.GetObjects("Choose Objects to Add to Block", preselect=True)
    if not objects: return
    
    block = rs.GetObject("Choose Block to Add Object to", rs.filter.instance)
    if not block: return
    
    rs.EnableRedraw(False)
    
    blockName = rs.BlockInstanceName(block)
    objref = rs.coercerhinoobject(block)
    idef = objref.InstanceDefinition
    idefIndex = idef.Index
    
    
    if rs.IsBlockReference(blockName):
        print "Block is referenced from file; unable to add object(s)"
        return
    
    blnCopy = False
    
    XformBlock = rs.BlockInstanceXform(block)

    rs.TransformObjects(objects, rs.XformInverse(XformBlock), blnCopy)
    
    objects.extend(rs.BlockObjects(blockName))
    
    newGeometry = []
    newAttributes = []
    for object in objects:
        newGeometry.append(rs.coercegeometry(object))
        ref = Rhino.DocObjects.ObjRef(object)
        attr = ref.Object().Attributes
        newAttributes.append(attr)
    
    InstanceDefinitionTable = sc.doc.ActiveDoc.InstanceDefinitions
    InstanceDefinitionTable.ModifyGeometry(idefIndex, newGeometry, newAttributes)
    
    rs.DeleteObjects(objects)
        
    rs.EnableRedraw(True)

AddToBlock()