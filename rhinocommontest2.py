# -*- coding: utf-8 -*-

import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino
import Rhino.Geometry



targId = rs.GetObject("Select the first object to replace", rs.filter.surface, preselect=True,)
#obj = sc.doc.Objects.Find(targId)
#if not targId:return
#point = rs.GetPointOnSurface(surface, "Point on surface")

obj = sc.doc.Objects.Find(targId)
srf = rs.coercesurface(targId)
#point = rs.GetPointOnSurface(srf, "Point on surface")
print srf

def intFlipBool(tf):
    return abs(tf-1)

def frange(start, count, step=1.0):
    ''' "range()" like function which accept float type''' 
    i = start
    for c in range(count):
        yield i
        i += step

def func(srf, dir, count):
    domains = []
    dom = srf.Domain(dir)
    print dom
    dist = dom.Length/count
    i = dist
    while i < dom.Length:
        domains.append(i)
        i = i+dist
    crvs = map(lambda x: srf.IsoCurve(intFlipBool(dir), x), domains)
    map(lambda x: sc.doc.Objects.AddCurve(x), crvs)
    return crvs

doms = func(srf, 1, 10)

print doms

#rs.AddPoint(point)

#dom1 = srf.Domain(0)
#dom2 = srf.Domain(1)
#print dom1
#print dom2
#print type(dom1)
#print dom1.Length

#b, u_parameter, v_parameter = srf.ClosestPoint(point)
#print b, u_parameter, v_parameter


#iso_curve = srf.IsoCurve(1, u_parameter)
#print iso_curve
#sc.doc.Objects.AddCurve(iso_curve)

