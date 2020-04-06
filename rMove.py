import rhinoscriptsyntax as rs
import trkRhinoPy as trp

def inputVector():
    p1 = rs.GetPoint("Pick first point")
    if p1:
        p2 = rs.GetPoint("Pick second point", p1)
    vec = p2 - p1
    return vec

inputvec = inputVector()
vector = inputvec

def rMove(vector):
    objs = rs.GetObjects("Select objs")
    if objs != None:
        rs.MoveObjects( objs, vector)
        objs = None
        vector = vector + inputvec
        rMove(vector)
rMove(vector)
