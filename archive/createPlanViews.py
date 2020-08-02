import rhinoscriptsyntax as rs
import ast

cutHeight = 1200

objdict = ast.literal_eval(rs.GetDocumentUserText("levels"))

def planClips(lvl):
    viewname = lvl["level"] + "_view"
    tempview = rs.AddNamedView( "tempview", "Top" )
    view = rs.AddNamedView( viewname, tempview )
    elevation = float(lvl["elevation"])
    lvlPlane = rs.CreatePlane((0,0,elevation))
    cutPlane = rs.PlaneFromNormal((0,0,elevation+cutHeight), (0,0,-1))
    planes = [lvlPlane, cutPlane]
    clips = [rs.AddClippingPlane(x, 1000, 1000, view) for x in planes]
    group = rs.AddGroup()
    rs.AddObjectsToGroup(clips, group)
    rs.DeleteNamedView(tempview)

map(planClips, objdict)

# def planClips(lvl):
#     viewname = lvl["level"] + "_view"
#     view = rs.AddNamedView( viewname, "Top" )
#     rs.RestoreNamedView( viewname, "Top" )
#     elevation = float(lvl["elevation"])
#     lvlPlane = rs.CreatePlane((0,0,elevation))
#     cutPlane = rs.PlaneFromNormal((0,0,elevation+cutHeight), (0,0,-1))
#     planes = [lvlPlane, cutPlane]
#     clips = [rs.AddClippingPlane(x, 1000, 1000, viewname) for x in planes]
#     group = rs.AddGroup()
#     rs.AddObjectsToGroup(clips, group)
#     rs.RestoreNamedView( "Top", viewname )
#     # rs.RestoreNamedView( viewname, "Top" )

# map(planClips, objdict)

# def planClips(lvl):
#     viewname = lvl["level"] + "_view"
#     elevation = float(lvl["elevation"])
#     lvlPlane = rs.CreatePlane((0,0,elevation))
#     cutPlane = rs.PlaneFromNormal((0,0,elevation+cutHeight), (0,0,-1))
#     planes = [lvlPlane, cutPlane]
#     clips = [rs.AddClippingPlane(x, 1000, 1000, "Top") for x in planes]
#     group = rs.AddGroup()
#     rs.AddObjectsToGroup(clips, group)
#     view = rs.AddNamedView( viewname, "Top" )
#     # rs.RestoreNamedView( viewname, "Top" )

# map(planClips, objdict)



# def planClips(lvl):
#     tempview = rs.AddNamedView( "tempview", "Top" )
#     rs.RestoreNamedView(tempview, "Top")
#     viewname = lvl["level"] + "_view"
#     elevation = float(lvl["elevation"])
#     lvlPlane = rs.CreatePlane((0,0,elevation))
#     cutPlane = rs.PlaneFromNormal((0,0,elevation+cutHeight), (0,0,-1))
#     planes = [lvlPlane, cutPlane]
#     clips = [rs.AddClippingPlane(x, 1000, 1000, tempview) for x in planes]
#     group = rs.AddGroup()
#     rs.AddObjectsToGroup(clips, group)
#     view = rs.AddNamedView( viewname, tempview)
#     rs.DeleteNamedView(tempview)

# map(planClips, objdict)

# cutHeight = 1200

# viewnames = []
# els = []

# userstr = rs.GetDocumentUserText("levels")
# objdict = ast.literal_eval(userstr)
# for i in objdict:
#     viewnames.append(i["level"]+ "_view")
#     els.append(float(i["elevation"]))

# pairs = zip(els, viewnames)

# def planClips(pairs):
#     planes = [rs.CreatePlane((0,0,pairs[0])), rs.PlaneFromNormal((0,0,pairs[0]+cutHeight), (0,0,-1))]
#     clips = [rs.AddClippingPlane(x, 1000, 1000, [pairs[1]]) for x in planes]
#     group = rs.AddGroup()
#     rs.AddObjectsToGroup(clips, group)

# map(planClips, pairs)






    # lvlname = lvl["level"]
    # viewname = lvlname + "_view"
    # view = rs.AddNamedView( viewname, "Top" )
    # print view
    # elevation = float(lvl["elevation"])

# def planClips(lvl):
#     lvlname = lvl["level"]
#     viewname = lvlname + "_view"
#     view = rs.AddNamedView( viewname, "Top" )
#     print view
#     elevation = float(lvl["elevation"])
#     lvlPlane = rs.CreatePlane((0,0,elevation))
#     cutPlane = rs.PlaneFromNormal((0,0,elevation+cutHeight), (0,0,-1))
#     planes = [lvlPlane, cutPlane]
#     clips = [rs.AddClippingPlane(x, 1000, 1000) for x in planes]
#     group = rs.AddGroup()
#     rs.AddObjectsToGroup(clips, group)




# def lvlPlanes():
#     userstr = rs.GetDocumentUserText("levels")
#     objdict = ast.literal_eval(userstr)
#     for i in objdict:
#         lvlnames.append(i["level"])
#         els.append(float(i["elevation"]))
#     # map(planClips, objdict)
# lvlPlanes()