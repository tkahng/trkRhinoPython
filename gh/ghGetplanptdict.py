"""Provides a scripting component.
    Inputs:
        x: The x script variable
        y: The y script variable
    Output:
        a: The a output variable"""

__author__ = "Tchunoo"
__version__ = "2020.08.09"

import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino as rc
#import ast
#import json

sc.doc = rc.RhinoDoc.ActiveDoc

objdict = sc.sticky['planptdict']

level = objdict.keys()
plane = map(lambda x:rs.CreatePlane(x, rs.WorldXYPlane().XAxis, rs.WorldXYPlane().YAxis), objdict.values())
