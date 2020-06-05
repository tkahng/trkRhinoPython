import rhinoscriptsyntax as rs
import trkRhinoPy as trp

# objs = rs.GetObjects('select objs', rs.filter.surface|rs.filter.curve|rs.filter.point|rs.filter.polysurface, preselect=True)
# grade = rs.GetString("toggle grade")
# point1 = rs.GetPoint("Pick first point")

rs.EnableRedraw(False)

def process():
    objs = rs.GetObjects('select objs', \
        rs.filter.surface|\
            rs.filter.curve|\
                rs.filter.point|\
                    rs.filter.polysurface, preselect=True)
    grade = rs.GetString("toggle grade")
    rs.EnableRedraw(False)
    isUG = trp.boolToggle(grade)
    groups = trp.groupByElevation(objs, isUG)
    # print type(groups)
    trp.setLevel(groups, isUG, trp.setLevelforObj)

def process2():
    objs = rs.GetObjects('select objs', \
    rs.filter.surface|\
        rs.filter.curve|\
            rs.filter.point|\
                rs.filter.polysurface, preselect=True)
    pt = rs.GetPoint("Pick first point")
    # isUG = trp.boolToggle(grade)
    pairs = map(trp.setObjZPair, objs)

    for pair in pairs:
        if pair[1] >= pt.Z:
            pair.append(False)
        else:
            pair.append(True)
    # gradelist = [(ag, False), (ug, True)]
    groups = trp.groupByElevation(objs, isUG)
    trp.setLevel(groups, isUG, trp.setLevelforObj)

if __name__ == '__main__':
    process()
    # process2(objs, grade, trp.setLevelforObj)    

rs.EnableRedraw(True)