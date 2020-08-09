"""Provides a scripting component.
    Inputs:
        x: The x script variable
        y: The y script variable
    Output:
        a: The a output variable"""

__author__ = "인시공현장PC"
__version__ = "2020.06.07"

import rhinoscriptsyntax as rs
import scriptcontext as sc

planptdict = dict(zip(levels, points))

sc.sticky["planptdict"] = planptdict