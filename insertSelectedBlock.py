import trkRhinoPy as trp
import rhinoscriptsyntax as rs

obj = rs.GetObject('select block to insert', rs.filter.instance, preselect=True)

if obj:
    blkname = rs.BlockInstanceName(obj)

    pt = rs.GetPoint('insertion point')

    if pt:
        rs.InsertBlock(blkname, pt)

