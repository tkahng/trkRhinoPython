import rhinoscriptsyntax as rs
import trkRhinoPy as trp

# rs.EnableRedraw(False)

def process():
    objs = rs.GetObjects('select objs', preselect=True)
    grade = rs.GetString("toggle grade")
    rs.EnableRedraw(False)
    isUG = trp.boolToggle(grade)
    groups = trp.groupByElevation(objs, isUG)
    trp.setLevel(groups, isUG, trp.setLevelforObj)

if __name__ == '__main__':
    process()

rs.EnableRedraw(True)