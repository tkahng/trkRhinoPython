import rhinoscriptsyntax as rs
import trkRhinoPy as trp

objs = rs.GetObjects('select objs', rs.filter.surface|rs.filter.curve|rs.filter.point, preselect=True)
grade = rs.GetString("toggle grade")

def process(objs, grade, func):
    isUG = trp.boolToggle(grade)
    groups = trp.groupByElevation(objs, isUG)
    trp.setLevel(groups, isUG, func)

if __name__ == '__main__':
    process(objs, grade, trp.setDictforDatum)  # Put the a call to the main function in the file.    