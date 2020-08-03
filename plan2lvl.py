import rhinoscriptsyntax as rs
import trkRhinoPy as trp
import scriptcontext as sc
import Rhino

objs = rs.GetObjects('select objects', preselect=True)

reverse = rs.GetString("reverse")

isreverse = trp.boolToggle(reverse)

lvlpts = sc.sticky["lvlptdict"]
planpts = sc.sticky['planptdict']

levelkeys = lvlpts.keys()

vecs = dict([(key, lvlpts[key] - planpts[key]) for key in levelkeys])

def lvlxform(obj):
    lvlkey = rs.GetUserText(obj, 'level')
    vec = vecs[lvlkey]
    if isreverse:
        vec = rs.VectorReverse(vec)
    rs.MoveObject(obj, vec)

if lvlpts and planpts and objs:
    map(lvlxform, objs)






# sc.doc = Rhino.RhinoDoc.ActiveDoc

# levels = sc.sticky["lvldict"]

# pts = rs.ObjectsByLayer('datums::plan pts', False)

# ptsk = map(lambda x:rs.GetUserText(x, 'level'), pts)
# p3ds = map(rs.CreatePoint, pts)

# def levelpt(d):
#     keys = d.keys()
#     coords = [(0,0,float(x['elevation'])) for x in d.values()]
#     pts = map(rs.CreatePoint, coords)
    
#     return dict(zip(keys, pts))

# levelkeys = levels.keys()


# lvlpts = levelpt(levels)

# planpts = dict(zip(ptsk, p3ds))



# sc.sticky['plan2lvlvec'] = vecs