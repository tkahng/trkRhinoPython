import rhinoscriptsyntax as rs
import os


all_views = rs.NamedViews() # a list of names (strings)
selected_views= rs.MultiListBox(all_views, message = "select views to save", defaults = all_views)

filename_base = rs.GetString("base file name","Rics_file_")
savepath = r"C:\Users\Tchunoo\Pictures"
# savepath = rs.BrowseForFolder(rs.DocumentPath(), "destination directory")
filepath = os.path.join(savepath, filename_base)

for view_name in selected_views:
    rs.RestoreNamedView(view_name)
    rs.Command('-_ViewCaptureToFile '+chr(34)+filepath+view_name+'.jpg'+chr(34)+' _EnterEnd')