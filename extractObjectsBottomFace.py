"""Returns the bottom faces of selected solids, and prints the sum area of the output faces. """

import rhinoscriptsyntax as rs
import trkRhinoPy as trp
# !-RunPythonScript "objectsBottomFace.py"

def inputFunc():
    """returns the selection

    Returns:
        ids: ids of selection
    """

    objs = rs.GetObjects("Select polysurface to explode", rs.filter.polysurface, preselect=True)
    return objs

# def calcArea(srfs):
#     areas = []
#     for srf in srfs:
#         areas.append(rs.SurfaceArea(srf)[0])
#     totalArea = sum(areas)
#     totalAreaPy = totalArea/3.3058
#     print totalArea, totalAreaPy
#     # txt = rs.ClipboardText(totalArea)

def outputFunc(objs):
    """Extracts the bottom faces of each solid in selection

    Args:
        objs (list of ids): list of ids

    Returns:
        list: list of bottom faces
    """

    rs.EnableRedraw(False)
    bottomFaces = []
    for obj in objs:
        resultFaces = trp.getBottomFace(obj)
        # print resultFaces
        for resultFace in resultFaces:
            trp.copySourceLayer(resultFace, obj)
            try:
                trp.copySourceData(resultFace, obj)
            except:
                pass
            bottomFaces.append(resultFace)
    rs.SelectObjects(bottomFaces)
    group = rs.AddGroup()
    rs.AddObjectsToGroup(bottomFaces, group)
    rs.EnableRedraw(True)
    return bottomFaces

def returnFaces():
    """runs the selection, extraction, and print calculation functions
    """    
    objs = inputFunc()
    rs.UnselectAllObjects()
    outputsrfs = outputFunc(objs)
    print trp.calcAreas(outputsrfs)

if __name__ == '__main__':
    returnFaces()