import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino

def RemoveFromBlock():
    block = rs.GetObject("Select Block to extract objects from", rs.filter.instance, preselect=True)
    if not block: return

    blockName = rs.BlockInstanceName(block)
    objref = rs.coercerhinoobject(block)
    idef = objref.InstanceDefinition
    idefIndex = idef.Index
    
    XformBlock = rs.BlockInstanceXform(block)
    blockObjects = rs.BlockObjects(blockName)
    blockInstanceObjects = rs.TransformObjects(blockObjects, XformBlock, True)
    
    objs = rs.GetObjects("Select Objects to extract from Block", objects =blockInstanceObjects)
    if not objs: 
        rs.DeleteObjects(blockInstanceObjects)
        return
    
    keep = [] #List to keep in block
    delete = [] #list to delete from block and add to doc
    
    rs.EnableRedraw(False)
    
    for object in blockInstanceObjects:
        if object in objs: delete.append(object)
        else: keep.append(object)
    
    if rs.IsBlockReference(blockName):
        print "Block is referenced from file; unable to modify block"
        rs.DeleteObjects(keep)
        return
    
    rs.TransformObjects(keep, rs.XformInverse(XformBlock), False)
    
    newGeometry = []
    newAttributes = []
    for object in keep:
        newGeometry.append(rs.coercegeometry(object))
        ref = Rhino.DocObjects.ObjRef(object)
        attr = ref.Object().Attributes
        newAttributes.append(attr)
    
    InstanceDefinitionTable = sc.doc.ActiveDoc.InstanceDefinitions
    InstanceDefinitionTable.ModifyGeometry(idefIndex, newGeometry, newAttributes)
    
    rs.DeleteObjects(keep)  
    rs.EnableRedraw(True)
   
RemoveFromBlock()