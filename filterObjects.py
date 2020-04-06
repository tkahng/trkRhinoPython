import rhinoscriptsyntax as rs

objs = rs.GetObjects("select objects", preselect=True)

def filterLayerStr(objs):
    text = rs.GetString("filter str")
    rs.UnselectAllObjects()
    output = [obj for obj in objs if text in rs.ObjectLayer(obj)]
    rs.SelectObjects(output)

filterLayerStr(objs)


