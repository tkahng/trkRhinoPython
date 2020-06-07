"""insert block from name of selected block
"""
import rhinoscriptsyntax as rs
import trkRhinoPy as trp


# walls = rs.GetObjects("Select solids", rs.filter.polysurface, preselect=True)
blks = rs.GetObjects("Select blocks", rs.filter.instance, preselect=True)

def func(obj):
    name = rs.BlockInstanceName(obj)
    


if blks:
    rs.EnableRedraw(False)
    [trp.resetBlockScale(blk) for blk in blks]
    rs.EnableRedraw(True)
