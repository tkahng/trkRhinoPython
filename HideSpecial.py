
import rhinoscriptsyntax as rs
import scriptcontext as sc


def HideSpecial():
    ids = rs.GetObjects("Select objects to hide.", preselect=True)
    if not ids:return
    
    sc.sticky['HIDE_SPECIAL'] = ids
    rs.HideObjects(ids)
    
    
HideSpecial()