import rhinoscriptsyntax as rs


obj = rs.GetObject("Pick any object")

rs.EnableRedraw(False)

layer = rs.ObjectLayer(obj)
parent = rs.ParentLayer(layer)
children = rs.LayerChildren(parent)

map(lambda x: rs.ObjectsByLayer(x, True), children)

rs.EnableRedraw(True)

# layers = rs.LayerNames()
# for layer in layers:
#     parent = rs.ParentLayer(layer)
#     print "Layer:", layer, ", Parent:", parent

# layers = rs.LayerNames()
# if layers:
#     layers  = rs.MultiListBox(layers, "Layers to lock")
# if layers:
#     for  layer in layers:
#         rs.LayerLocked(layer,  True)






