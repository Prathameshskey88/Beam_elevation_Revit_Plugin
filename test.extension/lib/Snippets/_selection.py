from Autodesk.Revit.DB import *


def get_selected(uidoc):
    selected_elements=[]
    #test
    if uidoc.Selection.GetElementIds():
        for elem_id in uidoc.Selection.GetElementIds():
            elem=uidoc.Document.GetElement(elem_id)
            selected_elements.append(elem_id)
    return selected_elements