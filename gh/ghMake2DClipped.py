import rhinoscriptsyntax as rs
import ghpythonlib.components as ghc
import Rhino.Geometry as rg
import scriptcontext as sc
import Rhino as rh

crv_vis = []
crv_hid = []
crv_clip = []
sil_type = []
curves = []

hd = rg.HiddenLineDrawingParameters()
hd.AbsoluteTolerance = sc.doc.ModelAbsoluteTolerance
for i in g:
    hd.AddGeometry(i,'')
hd.AddClippingPlane(pl)
hd.SetViewport(vp)

hl = rg.HiddenLineDrawing.Compute(hd,True)

flatten = rg.Transform.PlanarProjection(rs.WorldXYPlane())
page_box = hl.BoundingBox(True)
delta2D = rg.Vector2d(0,0)
delta2D = delta2D - rg.Vector2d(page_box.Min.X, page_box.Min.Y)
delta3D = rg.Transform.Translation(rg.Vector3d(delta2D.X, delta2D.Y, 0.0))
flatten = delta3D * flatten

a =  rg.SilhouetteType()
list = (a.Boundary, a.Crease, a.DraftCurve, a.MiscellaneousFeature, 
        None, a.NonSilhouetteCrease, a.NonSilhouetteSeam, a.NonSilhouetteTangent, 
        a.Projecting, a.SectionCut, a.Tangent, a.TangentProjects)

vis = rg.HiddenLineDrawingSegment.Visibility.Visible
hid = rg.HiddenLineDrawingSegment.Visibility.Hidden

for i,seg in enumerate(hl.Segments):
    if not seg.ParentCurve == None:
        crv = seg.CurveGeometry.DuplicateCurve()
        crv.Transform(flatten)
        curves.append(crv)
        
        for j in list:
            if seg.ParentCurve.SilhouetteType == j:
                sil_type.append(str(j))
        if seg.SegmentVisibility == vis:
            crv_vis.append(crv)
        elif seg.SegmentVisibility == hid:
            crv_hid.append(crv)


#sc.doc.Views.Redraw()