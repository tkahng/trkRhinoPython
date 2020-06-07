"""Special version for Robert - only uses lowest layer tree name for label"""
import rhinoscriptsyntax as rs

def SplitLayerName(name):
    #returns the lowest layer tree name, or full name if no parent
    if "::" in name:
        parts=name.split("::")
        return parts[-1]
    return name

def AddNameLayerGroupObj_Ex():
    objs=rs.GetObjects("Select objects to label",4+8+16+32+4096,preselect=True)
    if not objs: return
    for obj in objs:
        name=rs.ObjectName(obj)
        if not name: name="None"
        layer=rs.ObjectLayer(obj)
        layer=SplitLayerName(layer)
        bb=rs.BoundingBox(obj)
        text="Name: {}\nLayer: {}".format(name,layer)
        dot=rs.AddTextDot(text,(bb[0]+bb[6])/2)
        group=rs.AddGroup()
        rs.AddObjectsToGroup([obj,dot],group)
AddNameLayerGroupObj_Ex()
    