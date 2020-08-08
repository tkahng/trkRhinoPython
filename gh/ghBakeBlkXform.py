"""Provides a scripting component.
    Inputs:
        x: The x script variable
        y: The y script variable
    Output:
        a: The a output variable"""

__author__ = "인시공현장PC"
__version__ = "2020.08.09"

import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino

sc.doc = Rhino.RhinoDoc.ActiveDoc

def bakeblk(blkname, xform, bakename, idx):
    bakedblk = rs.InsertBlock2(blkname, xform)
    rs.SetUserText(bakedblk, bakename, idx)

def reset(bakename):
    rs.Command('SelKey '+bakename+' _Delete')

def func(xforms):
    bakename = 'BakeName('+bakeName+')'
    reset(bakename)
    for idx, xf in enumerate(xforms, start=1):
        bakeblk(name, xf, bakename, idx)
#    map(lambda x, y: bakeblk(name, x, bakename, y), xforms, idxs)



if bake is True:
    func(xform)
#
#if reset is True:
#    reset()