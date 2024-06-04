__title__="Select beams at a level"
__author__="SujitH"
__doc__="Hello button"
# -*- coding: utf-8 -*-
import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitServices')
clr.AddReference("System.Collections")

from Autodesk.Revit.DB import FilteredElementCollector, Level,ElementId, LocationCurve, FamilyInstance, BuiltInCategory
from RevitServices.Persistence import DocumentManager
from Snippets._selection import get_selected
from rpw import db, DB, UI, doc, uidoc
from System.Collections.Generic import List


if __name__=='__main__':
    #print("Hello BIM World1. Active view name:",name)
    print(get_selected(uidoc))

    #clearing selection
    # empty_element_ids = List[ElementId]()
    # uidoc.Selection.SetElementIds(empty_element_ids)
    
    col=FilteredElementCollector(doc)
    levels = col.OfClass(Level).ToElements()
    for lvl in levels:
        lvl_name = lvl.Name
        lvl_elevation = lvl.Elevation
        print("Level Name: {}, Elevation: {}".format(lvl_name, lvl_elevation))

    selected_elevation=levels[1].Elevation
    
    col=FilteredElementCollector(doc)
    beams=col.OfClass(FamilyInstance).OfCategory(BuiltInCategory.OST_StructuralFraming).ToElements()
    offset=4
    print("line36",len(beams))
    to_select=[]
    for beam in beams:
        z=beam.Location.Curve.GetEndPoint(0).Z
        print(z)
        if z<selected_elevation+offset and z>selected_elevation-offset:
            print(beam.Location.Curve.GetEndPoint(0), "To be selected")
            to_select.append(beam.Id)
        
    #select those beams only
    to_select=List[ElementId](to_select)
    print(to_select)
    uidoc.Selection.SetElementIds(to_select)
