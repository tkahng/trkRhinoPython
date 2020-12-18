import Rhino
import rhinoscriptsyntax as rs
import scriptcontext as sc

txt = rs.GetObject(message='select text', filter=512, preselect=True)

if rs.IsText(txt):
    text = rs.TextObjectText(txt)
    color = rs.ObjectColor(txt)

objs = rs.GetObjects(message='select objs', preselect=True)

def AddTag(obj, text, color):
    box = rs.BoundingBox(obj)
    mid = (box[0] + box[-2])/2
    tag = rs.AddTextDot(text, mid)
    rs.SetUserText(obj, 'tag', text)
    rs.ObjectColor(obj, color)
    group = rs.AddGroup()
    rs.AddObjectsToGroup([obj, tag], group)

if objs:
    map(lambda x: AddTag(x, text, color), objs)