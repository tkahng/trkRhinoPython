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

    lvlk = [x['level'] for x in levels]
    lvldict = dict(zip(lvlk, levels))
    lvlpt = [rs.CreatePoint((0,0,float(x['elevation']))) for x in levels]
    lvlptdict = dict(zip(lvlk, lvlpt))
    # pts = [" ".join(map(str,[0,0,float(x['elevation'])]))]
    # lvlptdict
    sc.sticky['lvlptdict'] = lvlptdict
    sc.sticky["lvldict"] = lvldict
    sc.sticky["levels"] = json.dumps(levels)
    rs.SetDocumentUserText("lvldict", json.dumps(lvldict))
    rs.SetDocumentUserText("levels", json.dumps(levels))
    # trp.cPlaneLvl()

if __name__ == '__main__':
    process(objs, grade, trp.setLevelforDatum)  

rs.EnableRedraw(True)