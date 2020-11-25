"""Provides a scripting component.
    Inputs:
        x: The x script variable
        y: The y script variable
    Output:
        a: The a output variable"""

__author__ = "trk"
__version__ = "2020.11.24"

import rhinoscriptsyntax as rs
import Rhino
import scriptcontext as sc

def BrepFootPrint(breps):
    edgecrvs = []

    for brep in breps:
        edgecrvs.extend([e.DuplicateCurve() for e in brep.Edges])

    
    # for brep in breps:
    #     edges.extend(brep.Edges)
        
    # edgecrvs = [e.DuplicateCurve() for e in edges]
    
#    flats = [Rhino.Geometry.Curve.ProjectToPlane(e, rs.WorldXYPlane()) for e in edgecrvs]
    
    crvregion = Rhino.Geometry.Curve.CreateBooleanRegions(edgecrvs, Rhino.Geometry.Plane.WorldXY, True, Rhino.RhinoDoc.ActiveDoc.ModelAbsoluteTolerance)
    
    outcrvs = []
    
    for i in range(crvregion.RegionCount):
        outcrvs.extend(crvregion.RegionCurves(i))
    return outcrvs



a = BrepFootPrint(breps)