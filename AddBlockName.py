import rhinoscriptsyntax as rs


def AddBlockName(obj):
    name = rs.BlockInstanceName(obj)
    pt = rs.BlockInstanceInsertPoint(obj)
    bb=rs.BoundingBox(obj)
    text=rs.AddText(name,(bb[0]+bb[6])/2)
    rs.SetUserText(text, 'tag', 'label')
    group=rs.AddGroup()
    rs.AddObjectsToGroup([obj, text], group)

objs=rs.GetObjects("Select objects to label", rs.filter.instance, preselect=True)

if objs:
    map(AddBlockName, objs)


# def AddNameLayerGroupObj():
#     objs=rs.GetObjects("Select objects to label",4+8+16,preselect=True)
#     if not objs: return
#     for obj in objs:
#         name=rs.ObjectName(obj)
#         if not name: name="None"
#         layer=rs.ObjectLayer(obj)
#         bb=rs.BoundingBox(obj)
#         text="Name: {}\nLayer: {}".format(name,layer)
#         dot=rs.AddTextDot(text,(bb[0]+bb[6])/2)
#         group=rs.AddGroup()
#         rs.AddObjectsToGroup([obj,dot],group)
# AddNameLayerGroupObj()
    