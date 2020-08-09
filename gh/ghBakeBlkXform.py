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
    comm = ('SelKey', bakename, '_Delete')
    s = ' '
    comstr = s.join(comm)
    print comstr
    rs.Command(comstr)

def func(xforms):
    namestr = ('BakeName(', bakeName, ')')
    sep = ''
    bakename = sep.join(namestr)
#    bakename = bakeName
    reset(bakename)
    for idx, xf in enumerate(xforms, start=1):
        bakeblk(name, xf, bakename, idx)
#    map(lambda x, y: bakeblk(name, x, bakename, y), xforms, idxs)



if bake is True:
    func(xform)
#
#if reset is True:
#    reset()