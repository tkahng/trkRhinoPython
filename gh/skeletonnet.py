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
import Rhino.Geometry as rg
import math
import clr
import os
import gc

clr.AddReferenceToFileAndPath('C:\Users\인시공현장PC\AppData\Roaming\Grasshopper\Libraries\StraightSkeletonNet.dll')


import StraightSkeletonNet as skel
import StraightSkeletonNet.Primitives as Ssk

def ptinpoly(pt, poly):
    tol = sc.doc.ModelAbsoluteTolerance
    if poly.Contains(pt, rs.WorldXYPlane(), tol) == Rhino.Geometry.PointContainment.Inside:
        return True
    else:
        return False

vertices2d = []

for seg in input.GetSegments():
    i = seg.From
    vertices2d.append(Ssk.Vector2d(i.X, i.Y))
    
vertices2ddotnet = List[Ssk.Vector2d](vertices2d)

sk = skel.SkeletonBuilder.Build(vertices2ddotnet)

polygons = []

for edgeResult in sk.Edges:
    controlPts = edgeResult.Polygon
    polylinePts = []
    for vector2d in controlPts:
        pt = Rhino.Geometry.Point3d(vector2d.X, vector2d.Y, 0)
        polylinePts.append(pt)
    polyline = Rhino.Geometry.Polyline(polylinePts)
    polygons.append(polyline)

skeleton = []

polycrv = input.ToPolylineCurve()

for poly in polygons:
    for seg in poly.GetSegments():
        if ptinpoly(seg.From, polycrv):
            skeleton.append(seg)

spine = []

for s in skeleton:
    if ptinpoly(s.From, polycrv) and ptinpoly(s.To, polycrv):
        spine.append(s)
    
c = spine

b = skeleton

a = polygons




