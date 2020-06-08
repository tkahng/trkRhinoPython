import rhinoscriptsyntax as rs
import trkRhinoPy as trp

key = rs.GetString("key", defaultString="level")
start = rs.GetInteger("starting value", number=1)

def rSet(val):
    objs = rs.GetObjects("Select objs")
    if objs:
        [rs.SetUserText(obj, key, str(val)) for obj in objs]
        group = rs.AddGroup()
        rs.AddObjectsToGroup(objs, group)
        # objs = None
        val = val + 1
        rSet(val)
rSet(start)
