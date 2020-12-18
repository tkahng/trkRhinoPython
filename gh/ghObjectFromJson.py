"""Provides a scripting component.
    Inputs:
        input: The x script variable
    Output:
        a: The a output variable"""

__author__ = "trk"
__version__ = "2020.12.19"

import rhinoscriptsyntax as rs
import json

mydicts = map(json.loads, input)

def AssignShape(desc):
    if desc.startswith('H-'):
        return 'H'
    elif 'H-' in desc:
        return 'SRC'
    else:
        return 'RC'

def ShapeDim(sh, dims):
    H_keys = ['h', 'b', 'ft', 'wt']
    RC_keys = ['b', 'h']
    if sh == 'H':
        return dict(zip(H_keys, dims))
    elif sh == 'RC':
        return dict(zip(RC_keys, dims))


descs = [x['desc'] for x in mydicts]

y = map(AssignShape, descs)

for i in mydicts:
    d = i['desc']
    sh = AssignShape(d)
    i['shape'] = sh
    dims = d.strip('H-').split('x')
    i['dimlist'] = dims
    shdim = ShapeDim(sh, dims)
    i['shapedims'] = shdim

a = json.dumps(mydicts)

class Dict2Obj(object):
    """
    Turns a dictionary into a class
    """
    #----------------------------------------------------------------------
    def __init__(self, dictionary):
        """Constructor"""
        for key in dictionary:
            setattr(self, key, dictionary[key])

