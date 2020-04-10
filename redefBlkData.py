import rhinoscriptsyntax as rs
import trkRhinoPy as trp
# walls = rs.GetObjects("Select solids", rs.filter.polysurface, preselect=True)
blk = rs.GetObject("Select blocks", rs.filter.instance, preselect=True)


objects = rs.BlockObjects(blk)
map(lambda x: rs.Area(x), objects)

# rs.EnableRedraw(False)
# trp.redefineBlockScale(blk)
# rs.EnableRedraw(True)

