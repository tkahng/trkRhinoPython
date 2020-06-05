import rhinoscriptsyntax as rs
import trkRhinoPy as trp

objs = rs.GetObjects('select objs', rs.filter.surface|rs.filter.curve|rs.filter.point|rs.filter.polysurface, preselect=True)
grade = rs.GetString("toggle grade")

rs.EnableRedraw(False)

def process(objs, grade, func):
    isUG = trp.boolToggle(grade)
    groups = trp.groupByElevation(objs, isUG)
    trp.setLevel(groups, isUG, func)
    [trp.setBrepHeight(obj) for obj in objs]

if __name__ == '__main__':
    process(objs, grade, trp.setLevelforDatum)  

rs.EnableRedraw(True)