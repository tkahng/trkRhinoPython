"""Provides a scripting component.
    Inputs:
        x: The x script variable
        y: The y script variable
    Output:
        a: The a output variable"""

__author__ = "trk"
__version__ = "2020.12.01"

from System.Collections.Generic import List
import rhinoscriptsyntax as rs
import scriptcontext as sc
import Grasshopper
import System
import random
import Rhino
import Rhino.Geometry
import math
import clr
import os
import gc

clr.AddReferenceToFileAndPath(dllpath)

#straightSkeleton_dll_loaded_Success = "StraightSkeletonNet" in [assembly.GetName().Name for assembly in clr.References]

#print straightSkeleton_dll_loaded_Success

#import StraightSkeletonNet as skel
#import StraightSkeletonNet.Primitives as Ssk

import StraightSkeletonNet
#import StraightSkeletonNet.Primitives

tol = sc.doc.ModelAbsoluteTolerance


def convertPolyline_to_polylineControlPts(polyline):
    controlPts = []
    for i in range(polyline.Count):
        pt = polyline.Item[i]
        controlPts.append(pt)
    
    return controlPts


def straightSkeleton_2DroofFaces(building_topSrf_brep):
    # based on: https://discourse.mcneel.com/t/straight-skeleton-implementation/63814/21
    
    brepZ_coord = building_topSrf_brep.Vertices[0].Location.Z  # breps are always planar so Z coordinate of all of them are the same
    
    # a) extract outer and inner (if existent) loops from 'building_topSrf_brep'
    building_topSrf_outerPolylines = []
    building_topSrf_innerPolylines = []
    for loop in building_topSrf_brep.Loops:
        # extract loop as a polyline
        loopCrv = loop.To3dCurve()
        loopPolyline_strongBox = clr.StrongBox[Rhino.Geometry.Polyline]()
        success = loopCrv.TryGetPolyline(loopPolyline_strongBox)
        polylineControlPts = convertPolyline_to_polylineControlPts(loopPolyline_strongBox)
        
        # determine if it is inside or outside loop
        if (loop.LoopType == Rhino.Geometry.BrepLoopType.Outer):
            building_topSrf_outerPolylines.extend(polylineControlPts[:-1])  # "[:-1]" always remove the last pt (equal to starting pt)
        else:
            building_topSrf_innerPolylines.append(polylineControlPts[:-1])  # "[:-1]" always remove the last pt (equal to starting pt)
    
    
    # b) convert outer and inner loops into ssVec 
    ssOuterLoop_VecL = []
    for controlPt in building_topSrf_outerPolylines:
        ssVec1 = StraightSkeletonNet.Primitives.Vector2d(controlPt.X, controlPt.Y)
        ssOuterLoop_VecL.append(ssVec1)
    
    ssInnerLoop_VecLL = List[List[StraightSkeletonNet.Primitives.Vector2d]]()
    for controlPtL in building_topSrf_innerPolylines:
        ssInnerLoop_VecL = List[StraightSkeletonNet.Primitives.Vector2d]()
        for controlPt in controlPtL:
            ssVec2 = StraightSkeletonNet.Primitives.Vector2d(controlPt.X, controlPt.Y)
            ssInnerLoop_VecL.Add(ssVec2)
        ssInnerLoop_VecLL.Add( ssInnerLoop_VecL )
    
    
    # c) create roof face polygons
    ssOuterLoop_VecL_dotNET = List[StraightSkeletonNet.Primitives.Vector2d](ssOuterLoop_VecL)
    ssInnerLoop_VecLL_dotNET = List[List[StraightSkeletonNet.Primitives.Vector2d]](ssInnerLoop_VecLL)
    try:
        sk = StraightSkeletonNet.SkeletonBuilder.Build(ssOuterLoop_VecL_dotNET, ssInnerLoop_VecLL_dotNET)
    except:
        return "sskeleton failed"
    
    
    # d) convert created roof face polygons into rhino polylines
    roof2DFacePolylines = []
    for edgeResult in sk.Edges:
        controlPts = edgeResult.Polygon
        polylinePts = []
        for vector2d in controlPts:
            pt = Rhino.Geometry.Point3d(vector2d.X, vector2d.Y, brepZ_coord)
            polylinePts.append(pt)
        
        # the outer loop polylines are closed. Therefore their first and last points coincide
        if (polylinePts[0].X == polylinePts[-1].X) and (polylinePts[0].X == polylinePts[-1].Y) and (polylinePts[0].X == polylinePts[-1].Z):
            # outer loop polyline
            polyline = Rhino.Geometry.Polyline(polylinePts)
        else:
            # inner loop polyline. they are never closed! Close them
            polyline = Rhino.Geometry.Polyline(polylinePts + [polylinePts[0]])
        
        roof2DFacePolylines.append(polyline)
    
    return roof2DFacePolylines

def ptonface(pt, face, relation):
    rc, u, v = face.ClosestPoint(pt)
    if rc:
        return face.IsPointOnFace(u, v) == relation

def SkeletonNet(inputbrep):
    inside = Rhino.Geometry.PointFaceRelation.Interior
    outside = Rhino.Geometry.PointFaceRelation.Exterior
    onborder = Rhino.Geometry.PointFaceRelation.Boundary
    brepface = inputbrep.Faces[0]
    polygons = straightSkeleton_2DroofFaces(inputbrep)
    spine = []
    skeleton = []
    
    for poly in polygons:
        for seg in poly.GetSegments():
            if not ptonface(seg.From, brepface, outside) and not ptonface(seg.To, brepface, onborder):
                skeleton.append(seg)
    
    for s in skeleton:
        if ptonface(s.From, brepface, inside) and ptonface(s.To, brepface, inside):
            spine.append(s)
    
    return polygons, skeleton, spine

Polygons, Skeleton, Spine = SkeletonNet(brep)