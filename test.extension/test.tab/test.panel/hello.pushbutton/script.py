# -*- coding: utf-8 -*-

__title__  = "List All Levels"
__author__  = "Pratham"
__doc__ = """Tool for level"""
#____________________________________________________________________ IMPORTS
import operator
from Autodesk.Revit.DB import (FilteredElementCollector,
                               BuiltInCategory,
                               UnitUtils)

app   = __revit__.Application
doc = __revit__.ActiveUIDocument.Document

#⬇️ IMPORTSrr
from Autodesk.Revit.DB import *
from pyrevit           import forms
from System.Collections.Generic import List

# #📦 VARIABLES
uidoc = __revit__.ActiveUIDocument
selection = uidoc.Selection
doc   = __revit__.ActiveUIDocument.Document

# FUNCTIONS
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
    '''PURPOSE:
    INPUT:
    OUTPUT: '''
    all_levels = FilteredElementCollector(doc).OfClass(Level).ToElements()
    dict_levels_by_name = {lvl.Name: lvl for lvl in all_levels}
    # dict_levels_by_elevation = {lvl.elevation: lvl.Elevation for lvl in all_levels}
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
    # User selects `Opt 1`, types 'Wood' in TextBox, and select Checkbox
# {'combobox1': 10.0, 'textbox1': 'Wood', 'checkbox': True}
user_input = get_user_input()
#create ui form for levels
new_select_level=user_input['select_level']
select_elevation=new_select_level.Elevation
print(select_elevation)
    # if offset == None:
    #     offset = 5
    # else:
offset = float(user_input['offset'])




all_beams = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructuralFraming).WhereElementIsNotElementType().ToElements()
to_select=[]
k_select=[]
s_select=[]
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

# uidoc.Selection.SetElementIds(to_select)

# # Refer_Level= INSTANCE_REFERENCE_LEVEL_PARAM


# print(res) # Print Selected Item

# for level in selected_levels:
#     print(level)
#
#     t = Transaction(doc, 'temp')
#     t.Start()
#     element_ids = doc.Delete(level.Id)
#
#     # 3️⃣ RollBack so level is not deleted!
#     t.RollBack()
#
#     # 4️⃣ Convert to Elements
#     elements = [doc.GetElement(e_id) for e_id in element_ids]
#
#     # 5️⃣ Print Unique Types
#     unique_types = {type(el) for el in elements}
#     print('{} has {} Dependant Elements.'.format(level.Name, len(elements)))
#     print('It includes {} unique Types'.format(len(unique_types)))
#     for typ in unique_types:
#         print(typ)
#
# all_levels = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements()
#
# selected_levels = forms.SelectFromList.show(all_levels,
#                                 multiselect=True,
#                                 name_attr='Name',
#                                 button_name='Select Levels')
# from pyrevit import forms
# items = ['POSITIVE', '0', 'NEGATIVE']
# res     = forms.SelectFromList.show(items,
#                 multiselect=True,
#                 button_name='Select Item')

#____________________________________________________________________ MAIN
# GET ALL LEVELS

# levels = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements()
#
# # CONVERT UNITS TO METERS
# dict_lvl = {}
# for i in levels:
#     # dict_lvl[i.Name] = convert_m_to_feet(i.Elevation)
#     dict_lvl[i.Name] = convert_internal_to_m(i.Elevation)
# # SORT BY ELEVATION
# sorted_x = sorted(dict_lvl.items(), key=operator.itemgetter(1))

# # PRINT LEVELS WITH ITS ELEVATIONS
# for i in sorted_x[::-1]: #reversed order
#     if i[1] > 0:
#         print("+{}		{}".format(format(i[1], '.2f'), i[0]))
#     elif i[1] < 0:
#         print("{}		{}".format(format(i[1], '.2f'), i[0]))
#     else:
#         print("{}		{}".format("0.00", i[0]))

# "05.04 - GetLevelDependantElements"
