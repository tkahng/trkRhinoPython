import rhinoscriptsyntax as rs
import trkRhinoPy as trp

objs = rs.GetObjects('select objects', preselect=True)
key = rs.GetString('key')

values = map(lambda x: rs.GetUserText(x, key), objs)

def func(a,b):
    return [a, b]
pairs = map(func, objs, values)

setpairs = set(map(lambda x:x[1], pairs))
newpairs = [[y[0] for y in pairs if y[1]==x] for x in setpairs]

for x in newpairs:
    group = rs.AddGroup()
    print rs.AddObjectsToGroup(x, group)