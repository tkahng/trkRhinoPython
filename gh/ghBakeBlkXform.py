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
import ghpythonlib.treehelpers as th
        
sc.doc = Rhino.RhinoDoc.ActiveDoc

def maptree(input):

    kvs = []
    for i in range(input.BranchCount):
        path = input.Path(i)
        data = list(input.Branch(path))
        for idx, val in enumerate(data):
            param = '{}({})'.format(str(path), str(idx))
            kv = dict(path=param, obj=val)
            kvs.append(kv)
    return kvs

def func(name, xform, bakeName):
    objpair = maptree(xform)
    
    idef = sc.doc.InstanceDefinitions.Find(name)
    idefx = idef.Index
    
    bakename = 'BakeName({})'.format(bakeName)
    
    objtbl = sc.doc.Objects
    
    existing = []
    
    for rhObj in objtbl:
        try:
            rawAtts = rhObj.Attributes.GetUserStrings()
            keys = rawAtts.AllKeys
            if bakename in keys:
                existing.append(rhObj)
        except:
            pass

    for rhObj in existing:
        try:
            objtbl.Delete(rhObj, False)
        except:
            pass
    
    newblk = []
    
    for kv in objpair:
        try:
            attr = Rhino.DocObjects.ObjectAttributes()
            attr.SetUserString(bakename, kv['path'])
            
            newblk.append(objtbl.AddInstanceObject(idefx, kv['obj'], attr))
        except:
            pass

if bake is True:
    func(name, xform, bakeName)