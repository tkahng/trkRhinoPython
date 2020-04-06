import rhinoscriptsyntax as rs
import trkRhinoPy as trp

objs = rs.GetObjects('select objs', rs.filter.surface, preselect=True)
# grade = rs.GetString("toggle grade")

rs.EnableRedraw(False)

map(trp.moveSrftoZ, objs)

# if __name__ == '__main__':
#     process(objs, grade, trp.setLevelforObj)  

rs.EnableRedraw(True)