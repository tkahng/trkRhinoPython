import rhinoscriptsyntax as rs
import trkRhinoPy as trp

objs = rs.GetObjects("Select Objects", preselect=True)

def mapstr(x):
    return str(x) + "\n"

def outputtext(obj):    
    kv = trp.sourceKeyValue(obj)
    zipbObj = zip(kv[0], kv[1])
    newstrs = map(mapstr, zipbObj)
    return ' '.join(newstrs)

def showeto(objs):
    strs = map(outputtext, objs)
    newstrs = map(mapstr, strs)
    rs.TextOut(' '.join(newstrs))

showeto(objs)