# import trkRhinoPy as trp
# import rhinoscriptsyntax as rs
# # from rhinopythonscripts.GeomTools import getSelected
# import scriptcontext as sc
# from rhinopythonscripts import Smart
# import Rhino as rc
#import Rhino
# import Rhino.Geometry as rg
# # import json
# # import ast
# # from _functools import reduce


import rhinoscriptsyntax as rs
import trkRhinoPy as trp

blockIds = rs.GetObjects("Pick Block", rs.filter.instance)

def blkObjs(blkid):
    blockName = rs.BlockInstanceName(blkid)
    objref = rs.coercerhinoobject(blkid)
    idef = objref.InstanceDefinition
    idefIndex = idef.Index
    print blockName, objref, idef, idefIndex


map(blkObjs, blockIds)
#def mirrorblk(blkid):
#    

#map(checkblkplane, blockIds)

# ids = rs.GetObjects()

# def alignNormal(id):
#     obj = sc.doc.Objects.Find(id)
#     geo = obj.Geometry
#     print geo
# #    srf = rs.coercesurface(id)
# #    print srf
#     srf = geo.Faces[0]
# #    srf = face.UnderlyingSurface()
#     print srf
#     normal = srf.NormalAt(srf.Domain(0).Mid, srf.Domain(1).Mid)
#     print normal
#     print normal.Z
#     if normal.Z < 0:
#         geo.Flip()
#         sc.doc.Objects.Replace(id, geo)
#         return id
# #        return rs.FlipSurface(id, True)
#     else:
#         return id

# map(alignNormal, ids)
    

#def FlipSurface(surface_id, flip=None):
#    """Returns or changes the normal direction of a surface. This feature can
#    also be found in Rhino's Dir command
#    Parameters:
#      surface_id (guid): identifier of a surface object
#      flip (bool, optional) new normal orientation, either flipped(True) or not flipped (False).
#    Returns:
#      vector: if flipped is not specified, the current normal orientation
#      vector: if flipped is specified, the previous normal orientation
#      None: on error
#    Example:
#      import rhinoscriptsyntax as rs
#      surf = rs.GetObject("Select object", rs.filter.surface)
#      if surf:
#          flip = rs.FlipSurface(surf)
#          if flip: rs.FlipSurface(surf, False)
#    See Also:
#      IsSurface
#    """
#    brep = rhutil.coercebrep(surface_id, True)
#    if brep.Faces.Count>1: return scriptcontext.errorhandler()
#    face = brep.Faces[0]
#    old_reverse = face.OrientationIsReversed
#    if flip!=None and brep.IsSolid==False and old_reverse!=flip:
#        brep.Flip()
#        surface_id = rhutil.coerceguid(surface_id)
#        if surface_id: scriptcontext.doc.Objects.Replace(surface_id, brep)
#        scriptcontext.doc.Views.Redraw()
#    return old_reverse



#tran = Rhino.Geometry.CurveOffsetCornerStyle

# objs = rs.GetObjects('select objects', preselect=True)

# groupbb = rs.ObjectsByLayer('planbb', False)

# def objBBPtPair(obj):
#     box = rs.BoundingBox(obj)
#     mid = (box[0] + box[-2])/2
#     return obj, mid


# def groupByBB(objs):
#     pairs = map(objBBPtPair, objs)

#     for bb in groupbb:
#         lvl = rs.GetUserText(bb, 'level')
#         for pair in pairs:
#             result = rs.PointInPlanarClosedCurve(pair[1], bb)
#             if result==1:
#                 rs.SetUserText(pair[0], "level", lvl)

# groupByBB(objs)


# def DuplicateEdgeCurves(object_id, select=False):
#     """Duplicates the edge curves of a surface or polysurface. For more
#     information, see the Rhino help file for information on the DupEdge
#     command.
#     Parameters:
#       object_id (guid): The identifier of the surface or polysurface object.
#       select (bool, optional):  Select the duplicated edge curves. The default is not
#       to select (False).
#     Returns:
#       list(guid, ..): identifying the newly created curve objects if successful.
#       None: if not successful, or on error.
#     Example:
#       import rhinoscriptsyntax as rs
#       obj = rs.GetObject("Select surface or polysurface", rs.filter.surface | rs.filter.polysurface)
#       if obj:
#           rs.DuplicateEdgeCurves( obj, True )
#           rs.DeleteObject( obj )
#     See Also:
#       IsPolysurface
#       IsSurface
#     """
#     brep = rhutil.coercebrep(object_id, True)
#     out_curves = brep.DuplicateEdgeCurves()
#     curves = []
#     for curve in out_curves:
#         if curve.IsValid:
#             rc = scriptcontext.doc.Objects.AddCurve(curve)
#             curve.Dispose()
#             if rc==System.Guid.Empty: return None
#             curves.append(rc)
#             if select: 
#                 rhobject = rhutil.coercerhinoobject(rc)
#                 rhobject.Select(True)
#     if curves: scriptcontext.doc.Views.Redraw()
#     return curves


# def DuplicateSurfaceBorder(surface_id, type=0):
#     """Create curves that duplicate a surface or polysurface border
#     Parameters:
#       surface_id (guid): identifier of a surface
#       type (number, optional): the border curves to return
#          0=both exterior and interior,
#          1=exterior
#          2=interior
#     Returns:
#       list(guid, ...): list of curve ids on success
#       None: on error
#     Example:
#       import rhinoscriptsyntax as rs
#       surface = rs.GetObject("Select surface or polysurface", rs.filter.surface | rs.filter.polysurface)
#       if surface: rs.DuplicateSurfaceBorder( surface )
#     See Also:
#       DuplicateEdgeCurves
#       DuplicateMeshBorder
#     """
#     brep = rhutil.coercebrep(surface_id, True)
#     inner = type==0 or type==2
#     outer = type==0 or type==1
#     curves = brep.DuplicateNakedEdgeCurves(outer, inner)
#     if curves is None: return scriptcontext.errorhandler()
#     tolerance = scriptcontext.doc.ModelAbsoluteTolerance * 2.1
#     curves = Rhino.Geometry.Curve.JoinCurves(curves, tolerance)
#     if curves is None: return scriptcontext.errorhandler()
#     rc = [scriptcontext.doc.Objects.AddCurve(c) for c in curves]
#     scriptcontext.doc.Views.Redraw()
#     return rc
#objs = rs.GetObjects('select objects', preselect=True)
#
#def objBBPtPair(obj):
#    box = rs.BoundingBox(obj)
#    mid = (box[0] + box[-2])/2
#    return obj, mid
#    # rs.addpoint
#
#def sortByAxis(objs, fn=lambda x:x[1].X, r=False):
#    pairs = map(objBBPtPair, objs)
#    sortedpairs = sorted(pairs, key=fn, reverse=r)
#    for idx, pairs in enumerate(sortedpairs, start=1):
#        rs.SetUserText(pairs[0], "level", str(idx))
#
#sortByAxis(objs, fn=lambda x:x[1].Y)






#obj = rs.GetObject('select objects', preselect=True)
#
#box = rs.BoundingBox(obj)
#
#
#
##print box
#
#
#def my_add(a, b):
##    print a, b
#    result = (a + b)
##    rs.AddPoint(result)
#    return result
#
#a = reduce(my_add, box)
#print a
##sc.doc = rc.RhinoDoc.ActiveDoc
##
##src = sc.sticky["levels"]
##
##lvldict = ast.literal_eval(src)
##
##lvlk = [x['level'] for x in lvldict]
##
##newdict = dict(zip(lvlk, lvldict))
##
##newdict2 = dict(map(lambda x: zip(x['level'], x), lvldict))
###lvlel = map(lambda x: zip(x['level'], x['elevation']), lvldict)
##
###lvlk = [x['level'] for x in lvldict]
###lvlk = [x['lelevation'] for x in lvldict]
##
###print lvlk, lvll
##print newdict2
##print newdict
##print lvlk
##print lvldict
###print type(lvlel)
##
#### objs = rs.GetObjects()
###targId = rs.GetObject("Select the first object to replace")
####if not targId:return
###
###rhobj = sc.doc.Objects.Find(targId)
####geo = obj.Geometry
###
###
###rhobjlist = getSelected()
###
###sf = Smart.RhinoObjectsToSmartFeatures(rhobjlist)
###
###print sf[0].attributes
###
#### import Rhino.Geometry
#### import Grasshopper as gh
###
#### gh.tree
###
#### import 
#### rs.GetObject()
