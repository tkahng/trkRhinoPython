import rhinoscriptsyntax as rs

objs = rs.GetObjects('select objs', preselect=True)
newParent = rs.GetString('new parent')


def swapParentLayer(obj):
    layer = rs.ObjectLayer(obj)
    if "::" in layer:
        splitlayer = layer.split("::")
        currentParent = splitlayer[0]
        newlayer = layer.replace(currentParent, newParent)
        rs.ObjectLayer(obj, newlayer)


# def swapParentLayer(obj):
#     currentParent = newParent
#     rs.ObjectLayer(obj, )

map(swapParentLayer, objs)
