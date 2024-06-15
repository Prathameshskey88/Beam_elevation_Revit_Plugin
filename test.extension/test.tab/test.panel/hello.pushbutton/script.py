# -*- coding: utf-8 -*-

__title__  = "List All Levels"
__author__  = "Pratham"
__doc__ = """Tool for level"""

#IMPORTS
import operator
from Autodesk.Revit.DB import (FilteredElementCollector,BuiltInCategory,UnitUtils)
from Autodesk.Revit.DB import *
from pyrevit           import forms
from System.Collections.Generic import List

#📦 VARIABLES
uidoc = __revit__.ActiveUIDocument
selection = uidoc.Selection
doc   = __revit__.ActiveUIDocument.Document
app   = __revit__.Application


# FUNCTIONS covertion of units need to shift this in library
# def convert_internal_to_m(length):
#     """Function to convert cm to feet."""
#     rvt_year = int(app.VersionNumber)
#     # RVT < 2022
#     if rvt_year < 2022:
#         from Autodesk.Revit.DB import DisplayUnitType
#         return UnitUtils.Convert(length,
#                                  DisplayUnitType.DUT_DECIMAL_FEET,
#                                  DisplayUnitType.DUT_METERS)
#     # RVT >= 2022
#     else:
#         from Autodesk.Revit.DB import UnitTypeId
#         return UnitUtils.ConvertFromInternalUnits(length, UnitTypeId.Meters)

def get_user_input():
    '''PURPOSE: selection of beam
    INPUT: selection of level, offset
    OUTPUT: selection of beam with in the range given by user'''
    all_levels = FilteredElementCollector(doc).OfClass(Level).ToElements()
    dict_levels_by_name = {lvl.Name: lvl for lvl in all_levels}
    # dict_levels_by_elevation = {lvl.elevation: lvl.Elevation for lvl in all_levels}
    #to use comboboxcomponent:
    # User selects `Opt 1`, types 'Wood' in TextBox, and select Checkbox
    # {'combobox1': 10.0, 'textbox1': 'Wood', 'checkbox': True}
    from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, Separator, Button, CheckBox)
    components = [Label('Select Level:'),
            ComboBox('select_level',dict_levels_by_name),
            Label('Enter offset/±Tolerence in mm:'),
            TextBox('offset', Text=""),
            CheckBox('checkbox1', 'by default Value'),
            Separator(),
            Button('Select')]
    form = FlexForm('Selection of Beam', components)
    form.show()
    if not form.values:
        forms.alert("No Levels Selected.\n Please try again", exitscript=True)
    return form.values
    
# assigning inpute values:
user_input = get_user_input()
#create ui form for levels
new_select_level=user_input['select_level']
select_elevation=new_select_level.Elevation
print(select_elevation)
    # to make by defalut value:
    # if offset == None:
    #     offset = 5
    # else:
offset = float(user_input['offset'])

#selection of beams with in range:
all_beams = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructuralFraming).WhereElementIsNotElementType().ToElements()
to_select=[]
k_select=[]
for refer_beam in all_beams:
    print(refer_beam.Id,type(refer_beam))
    z_value=refer_beam.Location.Curve.GetEndPoint(0).Z
    to_select.append(z_value)
    print(z_value)
    print (to_select)
    if z_value <= select_elevation + offset and z_value >= select_elevation - offset:
         # print(refer_beam.Location.Curve.GetEndPoint(0), "To be selected")
        print(select_elevation + offset)
        print(select_elevation - offset)
        k_select.append(refer_beam.Id)

k_select=List[ElementId](k_select)
print(k_select)
uidoc.Selection.SetElementIds(k_select)


