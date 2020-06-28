import rhinoscriptsyntax as rs
import trkRhinoPy as trp
import scriptcontext as sc
import json

objs = rs.GetObjects('select objs', rs.filter.surface|rs.filter.curve|rs.filter.point|rs.filter.polysurface, preselect=True)
grade = rs.GetString("toggle grade")

rs.EnableRedraw(False)

def process(objs, grade, func):
    
    isUG = trp.boolToggle(grade)
    groups = trp.groupByElevation(objs, isUG)

    trp.setLevel(groups, isUG, func)
    """setting lvldbdict as ordered for some reason
    """
    levels = [trp.createObjDict(x[0][0]) for x in groups]
    sc.sticky["levels"] = json.dumps(levels)
    rs.SetDocumentUserText("levels", json.dumps(levels))
    trp.cPlaneLvl()

if __name__ == '__main__':
    process(objs, grade, trp.setLevelforDatum)  

rs.EnableRedraw(True)