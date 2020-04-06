
import rhinoscriptsyntax as rs
import scriptcontext as sc


def ShowSpecial():
    ids = None
    if sc.sticky.has_key('HIDE_SPECIAL'):
        ids = sc.sticky['HIDE_SPECIAL']
    if ids:
        rs.EnableRedraw(False)
        for id in ids:
            rs.ShowObject(id)
        rs.EnableRedraw(True)

    if sc.sticky.has_key('HIDE_SPECIAL'):
        sc.sticky.pop('HIDE_SPECIAL')

ShowSpecial()