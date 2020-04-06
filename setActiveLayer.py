import rhinoscriptsyntax as rs
# !-RunPythonScript "setActiveLayer.py"
layer = rs.GetLayer("Select Layer", rs.CurrentLayer(), True, True)
if layer: rs.CurrentLayer(layer)
