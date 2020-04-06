import rhinoscriptsyntax as rs
objs = rs.GetObjects("Select Objects")
if objs:
    names = []
    for obj in objs:
        name = rs.ObjectName(obj)
        if name is None: name=""
        names.append(name)
    results = rs.PropertyListBox(objs, names, "Modify object name(s)")
    if results:
        for i in xrange(len(objs)):
            rs.ObjectName( objs[i], results[i] )