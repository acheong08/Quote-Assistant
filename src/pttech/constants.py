#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 14:46:00 2021

@author: jackhayley
"""

import os


# =============================================================================
# from enum import Enum
# 
# class Material(Enum):
#     """Enumerator for material type"""
#     STEEL = None
#     ALUMINUM = None
#     ZINC = None
# =============================================================================

# from tools import Standard

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates job temp folder and stores path in _MEIPASS
        import sys
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    print(os.path.join(base_path, relative_path))
    return os.path.join(base_path, relative_path)


def _insert_dict(m_obj1, m_obj2=('Diameter', 'Stepover', 'FRATE')):
    """Generates job dictionary based on given values and keys. In this case the
    program utilizes its default case to give job dictionary based on cutting
    info for each material type"""

    x_1, y_1, z_1 = map(str, m_obj2)
    x_2, y_2, z_2 = map(float, m_obj1)
    return {x_1: x_2, y_1: y_2, z_1: z_2}


def _get_super_dir(exponent, file=os.path.realpath(__file__)):
    if exponent > 0 and "_MEI" not in file:
        exponent -= 1
        directory = os.path.dirname(file)
        return _get_super_dir(exponent, directory)
    else:
        return file


print("SUPER DIR:", _get_super_dir(3))

APP_MODES = ('Material Costs', 'Machine Hours [UNTESTED]')

QUOTE_TYPES = ('3pc Draw Die Zinc', '2pc F/RS Zinc Tool', '2pc F/RS Steel Tool', '2pc F/RS Al Tool')
UNIT_TYPES = ('inch', 'millimeter')
MATERIAL_DENSITIES = {"Zinc": 0.25,
                      "Steel": 0.283,
                      "Aluminum": 0.1}

CIMATRON_LOCATORS = ('Box X:', 'Box Y:', 'Box Z:')

MAT_TOOLS_INFO = {'Steel': _insert_dict((0.741, 7.266, 3757.143)),
                  'Aluminum': _insert_dict((0.7395, 8.674285714, 3800.000)),
                  'Zinc': _insert_dict((0.894, 8.587, 4730.000))}
MATERIALS = tuple(MAT_TOOLS_INFO.keys())
MACHINES = ('GROB', 'HAAS2', 'OKK1', 'OKK2', 'VW1', 'VW2')
MAX_DIFFICULTY = 4
DIFFICULTIES = [str(n) for n in range(1, MAX_DIFFICULTY + 1)]
INIT_PARAMETERS = (('Quote', 'Material', 'Difficulty', 'Machine'),
                   ['Box X', 'Box Y', 'Box Z', 'Volume', 'Mass',
                    'Projected Area'])
FORM_WIDGET_NAMES = ('Quote #',
                     'Material Type',
                     'Difficulty Rating',
                     'Machine Model',
                     'CAD File (STEP)')
FORM_VALID_INPUTS = (MATERIALS,
                     [str(n) for n in range(MAX_DIFFICULTY + 1)],
                     MACHINES,
                     ('.stp', '.step'))

FORM_ERRORS = {'Material': 'Invalid material',
               'Difficulty': 'Difficulty out of range',
               'Machine': 'Invalid machine',
               'File': 'File not inputted'}
FORM_UNITS = (('', '', '', ''),
              ('mm', 'mm', 'mm', 'mm³', 'mm²', 'mm³', '', '', 'mm³/min',
               'hours'))
# Placeholder values for later redefinition
RSPEED_AV = 15000
# Base feedrate:non-feedrate ratio - estimate from Kevin
FRATE_RATIO = 0.85
FRATE_VAR = -0.05
PCT_ERROR = 0.334
BASE_CUT_INFO = 41092.19452
# Determine analysis order for calculations
ANALYSIS_ORDER = ('Volume To Remove',
                  'Estimated FR Ratio',
                  'Percent Error',
                  'Cut Rate',
                  'Time Required')


TOOLS = resource_path('resources/data/tools.json')

try:
    from sys import _MEIPASS
    VERSION = resource_path('resources/data/version.json')
except:
    VERSION = resource_path(str(_get_super_dir(3)
                                + '/resources/data/version.json'))

TEMP_OBJ = resource_path('resources/data/temp_obj.stl')

LOGO_PNG = resource_path('resources/images/logo.png')

TOOL_TYPES = {'Tip-radius': 'tip', 'Ball-nose': 'bll', 'Drill': 'djt'}

print("VER:", VERSION)
