import rhinoscriptsyntax as rs
import trkRhinoPy as trp

objs = rs.GetObjects('select objects', preselect=True)

def setUID(objs):
    for idx, obj in enumerate(objs, start=1):
        rs.SetUserText(obj, 'uid', 'uid-{}'.format(idx))

setUID(objs)

# def setQuickTag(obj, tagVal):
#     rs.SetUserText(obj, 'tag', tagVal)

# def getQuickTag(tagVal):
#     rs.Command('_SelKeyValue tag {}'.format(tagVal))

# def objsSetQuickTag():
#     objs = rs.GetObjects('select objects to tag', preselect=True)
#     tagVal = rs.GetString('Tag Value')
#     map(lambda x: setQuickTag(x, tagVal), objs)

# def objsGetQuickTag():
#     tagVal = rs.GetString('Tag Value')
#     rs.Command('_SelKeyValue tag {}'.format(tagVal))