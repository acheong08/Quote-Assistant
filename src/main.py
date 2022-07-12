#!/usr/bin/env python3
import time
from typing import Tuple

from application import App

from application.utils import *
from application.gui import *
from pttech.constants import *

from pttech.calculations import *


class Master(App):
    selected_input: StringVar
    mat_placeholder_excel_devpath = resource_path('resources/documents/placeholder_mat.xlsx')
    cut_placeholder_excel_devpath = resource_path('resources/documents/placeholder_cut.xlsx')
    config_json_devpath = resource_path('resources/documents/config.json')
    logo_devpath = resource_path('resources/images/logo.png')

    title_header = [LabelCustom('PT TECH UTILITY', fg_color=MASTER_THEME['fgh'], font_size=50, w=15),
                    0.5, 0.05]

    def __init__(self):
        self.default_geometry = (500, 500)
        self.large_geometry = (1250, 750)
        self.medium_geometry = (1000, 750)
        menu = ScreenUtil('menu', self.default_geometry,
                          ms_header=[LabelCustom('PT TECH UTILITY', fg_color=MASTER_THEME['fgh'], font_size=50, w=15,
                                                 height=2),
                                     0.5, 0.1],
                          mod_label=[LabelCustom('Select Mode'),
                                     0.5, 0.4],
                          mod_input=[OptionMenuCustom(*APP_MODES, w=25),
                                     0.5, 0.5])
        home_mat = ScreenUtil('home_mat', self.large_geometry,
                              ms_header=Master.title_header,
                              # md_header=[OptionMenuCustom(*APP_MODES, w=21, font_size=8, default_text=''),
                              #            0.9, 0.05],
                              dt_header=[LabelCustom('Tool Details', fg_color=MASTER_THEME['fgh'], font_size=36),
                                         0.25, 0.2],
                              qte_label=[LabelCustom('Tool Name'),
                                         0.15, 0.3],
                              qte_input=[InputCustom(),
                                         0.35, 0.3],
                              typ_label=[LabelCustom('Job Type'),
                                         0.15, 0.4],
                              typ_input=[OptionMenuCustom(*QUOTE_TYPES),
                                         0.35, 0.4],
                              prc_label=[LabelCustom('Precision'),
                                         0.15, 0.5],
                              prc_input=[OptionMenuCustom(*DIFFICULTIES),
                                         0.35, 0.5],
                              cb_button=[CheckbuttonCustom('Combo'),
                                         0.25, 0.65],
                              cf_button=[ButtonCustom(self.set_config, 'Config', 20, 1, 'white', 'black'),
                                         0.25, 0.9],
                              # mn_button=[ButtonCustom(self.reset_menu, 'Back to\nMenu', 10, 2),
                              #            0.25, 0.9],
                              io_header=[LabelCustom('Tool Input', fg_color=MASTER_THEME['fgh'], font_size=36),
                                         0.75, 0.2],
                              dim_radio=[RadioButtonsCustom('Excel File', 'Manual Input'),
                                         0.75, 0.3],
                              fl_button=[FileButtonCustom(self.save_data_excel, data_type='xlsx'),
                                         0.75, 0.5, 0],
                              dmx_label=[LabelCustom('Length', w=5),
                                         0.65, 0.45, 0],
                              dmy_label=[LabelCustom('Width', w=5),
                                         0.75, 0.45, 0],
                              dmz_label=[LabelCustom('Height', w=5),
                                         0.85, 0.45, 0],
                              dmx_input=[InputCustom(w=5),
                                         0.65, 0.55, 0],
                              dmy_input=[InputCustom(w=5),
                                         0.75, 0.55, 0],
                              dmz_input=[InputCustom(w=5),
                                         0.85, 0.55, 0],
                              msm_label=[LabelCustom('Units'),
                                         0.65, 0.65],
                              msm_input=[OptionMenuCustom(*UNIT_TYPES, w=13),
                                         0.85, 0.65],
                              xp_button=[ButtonCustom(self.set_export, 'Export', 10, 2),
                                         0.75, 0.9])

        export_mat = ScreenUtil('export_mat', self.large_geometry,
                                # md_header=[OptionMenuCustom(*APP_MODES, w=21, font_size=8, default_text=''),
                                #            0.9, 0.05],
                                exp_label=[LabelCustom(),
                                           0.5, 0.1],
                                cst_label=[LabelCustom(),
                                           0.5, 0.2],
                                xcl_label=[LabelCustom('Excel Manager', font_size=32),
                                           0.5, 0.5],
                                xcl_input=[LabelCustom('ok.', font_size=14, w=30),
                                           0.5, 0.6],
                                ae_button=[ButtonCustom(self.append_data, 'Add Entry', 8, 1),
                                           0.35, 0.7],
                                xp_button=[ButtonCustom(self.export_data, 'Export', 8, 1),
                                           0.5, 0.7],
                                re_button=[ButtonCustom(self.reset_data, 'Reset Entries', 13, 2, font_size=16),
                                           0.65, 0.7],
                                rt_button=[ButtonCustom(self.return_home, 'Return', 10, 2),
                                           0.3, 0.9],
                                rs_button=[ButtonCustom(self.reset_home, 'Reset Form', 10, 2),
                                           0.7, 0.9])

        config_mat = ScreenUtil('config_mat', self.large_geometry,
                                # md_header=[OptionMenuCustom(*APP_MODES, w=21, font_size=8, default_text=''),
                                #            0.9, 0.05],
                                sc1_label=[LabelCustom('Steel Cost per pound'),
                                           0.25, 0.2],
                                sc1_input=[InputCustom(),
                                           0.75, 0.2],
                                zc1_label=[LabelCustom('Zinc Cost per pound'),
                                           0.25, 0.3],
                                zc1_input=[InputCustom(),
                                           0.75, 0.3],
                                ac1_label=[LabelCustom('Aluminum Cost per pound'),
                                           0.25, 0.4],
                                ac1_input=[InputCustom(),
                                           0.75, 0.4],
                                sc2_label=[LabelCustom('Steel Cost per hour'),
                                           0.25, 0.5],
                                sc2_input=[InputCustom(),
                                           0.75, 0.5],
                                zc2_label=[LabelCustom('Zinc Cost per hour'),
                                           0.25, 0.6],
                                zc2_input=[InputCustom(),
                                           0.75, 0.6],
                                ac2_label=[LabelCustom('Aluminum Cost per hour'),
                                           0.25, 0.7],
                                ac2_input=[InputCustom(),
                                           0.75, 0.7],

                                rt_button=[ButtonCustom(self.update_config, 'Update', 10, 2),
                                           0.5, 0.9])

        home_cut = ScreenUtil('home_cut', self.medium_geometry,
                              ms_header=Master.title_header,
                              md_header=[OptionMenuCustom(*APP_MODES, w=21, font_size=8, default_text=''),
                                         0.9, 0.05],
                              qte_label=[LabelCustom("Tool"),
                                         0.35, 0.25],
                              qte_input=[InputCustom(),
                                         0.65, 0.25],
                              mat_label=[LabelCustom("Material"),
                                         0.35, 0.35],
                              mat_input=[OptionMenuCustom(*MATERIALS),
                                         0.65, 0.35],
                              prc_label=[LabelCustom("Precision"),
                                         0.35, 0.45],
                              prc_input=[OptionMenuCustom(*DIFFICULTIES),
                                         0.65, 0.45],
                              fil_label=[LabelCustom("Cimatron File"),
                                         0.35, 0.55],
                              fl_button=[FileButtonCustom(self.save_data_excel, data_type='xlsx'),
                                         0.65, 0.55],
                              mn_button=[ButtonCustom(self.reset_menu, 'Back to\nMenu', 10, 2),
                                         0.25, 0.9],
                              xp_button=[ButtonCustom(self.set_export, 'Export', 10, 2),
                                         0.75, 0.9])

        export_cut = ScreenUtil('export_cut', self.large_geometry,
                                md_header=[OptionMenuCustom(*APP_MODES, w=21, font_size=8, default_text=''),
                                           0.9, 0.05],
                                exp_label=[LabelCustom(),
                                           0.5, 0.4],
                                cst_label=[LabelCustom(),
                                           0.5, 0.5],
                                ae_button=[ButtonCustom(self.append_data, 'Add Entry', 8, 1),
                                           0.35, 0.7],
                                xp_button=[ButtonCustom(self.export_data, 'Export', 8, 1),
                                           0.5, 0.7],
                                re_button=[ButtonCustom(self.reset_data, 'Reset Entries', 13, 2, font_size=16),
                                           0.65, 0.7],
                                rt_button=[ButtonCustom(self.return_home, 'Return', 10, 2),
                                           0.3, 0.9],
                                rs_button=[ButtonCustom(self.reset_home, 'Reset Form', 10, 2),
                                           0.7, 0.9])

        self.m_import = ExcelIO()
        self.m_export = ExcelIO()
        self.m_config = JsonIO()
        self.m_data = DataHandler()
        self.m_calc = MasterCalculations()

        self.m_config.set_file(Master.config_json_devpath)

        self.exported = False

        assert isinstance(self.m_calc(Material), Material)
        assert isinstance(self.m_calc(Cutting), Cutting)

        super().__init__(title='Quote Assistant',
                         dimensions=self.default_geometry,
                         lock=True,
                         logo=Master.logo_devpath,
                         screens=[
                                  # menu(),
                                  home_mat(),
                                  export_mat(),
                                  config_mat(),
                                  home_cut(),
                                  export_cut()
                         ])

    def periodic(self):
        # self.check_screen_selection() if self.m_screen.current_screen is self.m_screen('menu') else \
        #     self.set_current_screen()
        self.check_input_selection() if self.m_screen.current_screen is self.m_screen('home_mat') else \
            self.update_excel_selection() if self.m_screen.current_screen is self.m_screen('export_mat') else None
    def get_mode(self, shorthand=False):
        for n, mode in enumerate(APP_MODES):
            if self.m_screen().get_name()[-3:] in mode.lower():
                return APP_MODES[n] if not shorthand else self.m_screen().get_name()[-3:]
        return self.m_screen().get_name()

    def reset_menu(self):
        self.m_screen('menu').reset_screen()
        self.window.geometry('500x500')

    def save_data_excel(self, path):
        self.m_import.set_file(path)
        print(self.m_screen().get_name())
        self.m_import.extract_data(CIMATRON_LOCATORS[self.m_screen().get_name()[-3:]], offset=(1, 0))
        self.m_data.set_dimensions(tuple(self.m_import.get_data()[:3]))
        if self.get_mode() == APP_MODES[1]:
            self.m_data.set_volume(self.m_import.get_data()[3])

        print(self.m_data.get_dimensions(), '|', self.m_data.get_volume())

    def save_data_manual(self):
        # noinspection PyTypeChecker
        self.m_data.set_dimensions(tuple([float(self.m_screen().widgets[str('dm' + n + '_input')].get_value(float))
                                          for n in ('x', 'y', 'z')]))

    def set_config(self):
        data = self.m_config.get_entries()
        self.m_screen('config_mat').widgets['sc1_input'].set_value(data['cost_per_pound_steel'])
        self.m_screen('config_mat').widgets['zc1_input'].set_value(data['cost_per_pound_zinc'])
        self.m_screen('config_mat').widgets['ac1_input'].set_value(data['cost_per_pound_aluminum'])
        self.m_screen('config_mat').widgets['sc2_input'].set_value(data['cost_per_hour_steel'])
        self.m_screen('config_mat').widgets['zc2_input'].set_value(data['cost_per_hour_zinc'])
        self.m_screen('config_mat').widgets['ac2_input'].set_value(data['cost_per_hour_aluminum'])
        self.m_screen('config_mat').set_screen()

    def update_config(self):
        self.m_config.edit_entry('cost_per_pound_steel',
                                 self.m_screen('config_mat').widgets['sc1_input'].get_value(float))
        self.m_config.edit_entry('cost_per_pound_zinc',
                                 self.m_screen('config_mat').widgets['zc1_input'].get_value(float))
        self.m_config.edit_entry('cost_per_pound_aluminum',
                                 self.m_screen('config_mat').widgets['ac1_input'].get_value(float))
        self.m_config.edit_entry('cost_per_hour_steel',
                                 self.m_screen('config_mat').widgets['sc2_input'].get_value(float))
        self.m_config.edit_entry('cost_per_hour_zinc',
                                 self.m_screen('config_mat').widgets['zc2_input'].get_value(float))
        self.m_config.edit_entry('cost_per_hour_aluminum',
                                 self.m_screen('config_mat').widgets['ac2_input'].get_value(float))

        self.reset_home()

    def return_home(self):
        self.m_calc = MasterCalculations()
        self.set_home()

    def reset_home(self):
        self.m_data = DataHandler()
        self.m_calc = MasterCalculations()
        print(self.get_mode(True))
        self.m_screen('home_' + self.get_mode(True)).reset_screen()

    def set_home(self):
        self.m_screen('home_' + self.get_mode(True)).set_screen()

    def set_export(self):
        if not self.process_data():
            return
        if self.get_mode() == APP_MODES[0]:
            self.m_screen('export_mat').widgets['exp_label'].set_value('Total Volume: ' + str(round(self.m_calc(
                    Material).required_volume, 2)))
            self.m_screen('export_mat').widgets['cst_label'].set_value('Total Material Cost: ~$'
                                                                       + str(round(self.m_data.get_cost('mat'), 2)))
            self.m_screen('export_mat').set_screen()
        elif self.get_mode() == APP_MODES[1]:
            # self.m_screen('export_cut').widgets['exp_label'].set_value('Total Volume: ' + str(round(self.m_calc(
            #         Material).required_volume, 2)))
            self.m_screen('export_cut').widgets['cst_label'].set_value('Total cost in hours: ~' + str(self.m_calc(
                    Cutting).get_cost()))
            self.exported = False
            self.m_screen('export_cut').set_screen()

    def process_data(self):
        try:
            if not self.m_screen().widgets['fl_button'].is_file_inputted():
                self.save_data_manual()
            print("---MODE: ", self.get_mode())
            self._process_mat_calc() if self.get_mode() == APP_MODES[0] else self._process_cut_calc() if \
                self.get_mode() == APP_MODES[1] else None
        except (ValueError, KeyError) as e:
            self.m_error.display('Not all fields are filled out correctly!\nPlease try again.')
            return False
        self._export_mat_calc() if self.get_mode() == APP_MODES[0] else self._export_cut_calc() if self.get_mode() == \
            APP_MODES[1] else None
        return True

    def _process_mat_calc(self):
        print("--ATTEMPTING: Type")
        self.m_data.set_type(self.m_screen().widgets['typ_input'].get_value())
        print("--ATTEMPTING: conversion")
        self.m_data.set_conversion(self.m_screen().widgets['msm_input'].get_value())
        print("--ATTEMPTING: Tool")
        self.m_data.set_tool(self.m_screen().widgets['qte_input'].get_value())
        print("--ATTEMPTING: Precision")
        self.m_data.set_precision(self.m_screen().widgets['prc_input'].get_value())
        print("--ATTEMPTING: Combo")
        self.m_data.set_combo(self.m_screen('home_mat').widgets['cb_button'].get_value())
        print(self.m_data.get_combo())
        print("GOT JOB TYPE:", self.m_data.get_type())
        print("GOT DATA TYPE:", self.m_data.get_conversion())
        print("GOT COMBO TYPE:", self.m_data.get_combo())
        print("GOT DIMS:", self.m_data.get_dimensions())
        print("--ATTEMPTING: Calculation")
        self.m_calc(Material).calculate_cost(QUOTE_TYPES.index(self.m_data.get_type()),
                                             self.m_data.get_dimensions(),
                                             self.m_data.get_conversion(),
                                             self.m_data.get_precision(),
                                             self.m_data.get_combo(),
                                             self.m_config.get_entries())
        self.m_data.set_volume(round(self.m_calc(Material).get_volume(), 2))
        self.m_data.set_block(self.m_calc(Material).get_block())
        self.m_calc(Cutting).calculate_cost(QUOTE_TYPES.index(self.m_data.get_type()),
                                            self.m_data.get_block(),
                                            self.m_data.get_volume(),
                                            self.m_data.get_precision(),
                                            self.m_data.get_conversion(),
                                            self.m_data.get_combo(),
                                            self.m_config.get_entries())
        self.m_data.set_hours(round(self.m_calc(Cutting).get_time(), 2))

    def _process_cut_calc(self):
        print("--ATTEMPTING: Tool")
        self.m_data.set_tool(self.m_screen().widgets['qte_input'].get_value())
        print("--ATTEMPTING: Material")
        self.m_data.set_type(self.m_screen().widgets['mat_input'].get_value())
        print("--ATTEMPTING: Precision")
        self.m_data.set_precision(self.m_screen().widgets['prc_input'].get_value())
        self.m_data.set_conversion(UNIT_TYPES[1])
        self.m_calc(Cutting).calculate_cost(self.m_data.get_type(),
                                            self.m_data.get_dimensions(),
                                            self.m_data.get_volume(),
                                            self.m_data.get_precision(),
                                            self.m_data.get_conversion())

    def _export_mat_calc(self):
        self.m_data.set_cost(round(self.m_calc(Material).get_cost(), 2), 'mat')
        self.m_data.set_cost(round(self.m_calc(Cutting).get_cost(), 2), 'cut')
        self.m_data.set_cost(round(self.m_calc.get_cumulative_cost(), 2))

    def _export_cut_calc(self):
        self.m_data.set_additionals(self.m_calc(Cutting).get_additional_values)
        self.m_data.set_cost(self.m_calc(Cutting).get_cost())

    def append_data(self):
        self.exported = False
        self.m_data.add_entry(self.m_data.get_data(self.get_mode(True)))
        print("-ADDED ENTRY")

    def export_data(self):
        from datetime import datetime as dt
        from pathlib import Path as pt

        # self.append_data()

        entries = self.m_data.get_entries()
        print("EXPORT ENTRIES:\n", entries)
        quote_info = self.m_data.get_tool() if len(entries) == 1 and entries[0][0] != '' else "Quotes"
        file = Master.mat_placeholder_excel_devpath if self.get_mode() == APP_MODES[0] else \
            Master.cut_placeholder_excel_devpath if self.get_mode() == APP_MODES[1] else ''
        self.m_export.create_file(file,
                                  str(pt.home()
                                      / 'Downloads'
                                      / str(
                                          '[' + quote_info + '] '
                                          + dt.now().strftime(" %Y-%m-%d  ""%H-%M-%S")
                                          + '.xlsx')))
        for index, entry in enumerate(entries):
            self.m_export.manipulate_file(entry, index + 3)
        self.exported = True
        print("-EXPORTED ALL ENTRIES")

    def reset_data(self):
        self.exported = False
        self.m_data.reset_entries()

    flag = True

    def set_current_screen(self):
        screen = self.m_screen().get_name()
        array = ['mat', 'cut']
        modes = [*APP_MODES]

        for index, item in enumerate(array):
            if item in self.m_screen().get_name():
                temp = modes[index]
                array.remove(item)
                modes.pop(index)
                array.append(item)
                modes.append(temp)

        for index, search in enumerate(array):
            value = self.m_screen().widgets['md_header'].get_value().lower()
            # time.sleep(0.5)
            if self.m_screen.transitioning:
                # print("Case 1")
                # time.sleep(0.5)
                continue
            elif search not in value and search not in screen:
                # print("Case 1.5")
                Master.flag = True
                continue
            elif search in value:
                # print(value)
                if search in screen:
                    # print("Case 2")
                    Master.flag = False
                    continue
                # print('value:', value)
                # print('screen:', screen)
                self.m_screen('home_' + search).reset_screen()
                for index, item in enumerate(array):
                    if item in self.m_screen().get_name():
                        temp = modes[index]
                        array.remove(item)
                        modes.pop(index)
                        array.append(item)
                        modes.append(temp)
                # print("Case 3")
                Master.flag = True
                break
            elif search in screen and Master.flag:
                self.m_screen().widgets['md_header'].set_value(modes[index])
                # print("Case 4")
                break

    def check_screen_selection(self):
        observed_state = self.m_screen('menu').widgets['mod_input'].get_value()
        self.m_screen('home_mat').reset_screen() if observed_state == APP_MODES[0] else \
            self.m_screen('home_cut').reset_screen() if observed_state == APP_MODES[1] else None

    def check_input_selection(self):
        widgets_a = ['fl_button']
        widgets_b = ['dmx_label', 'dmy_label', 'dmz_label', 'dmx_input', 'dmy_input', 'dmz_input']
        observed_state = self.m_screen('home_mat').widgets['dim_radio'].get_selection()
        previous_state = self.m_screen('home_mat').widgets['dim_radio'].previous_state
        if observed_state != previous_state:
            self.m_screen('home_mat').widgets['dim_radio'].previous_state = observed_state
            if observed_state == '0':
                for widget in widgets_a:
                    self.m_screen('home_mat').widgets[widget].toggle_state = 1
                    self.m_screen('home_mat').widgets[widget].toggle_widget(1)
                for widget in widgets_b:
                    self.m_screen('home_mat').widgets[widget].toggle_state = 0
                    self.m_screen('home_mat').widgets[widget].toggle_widget(0)
            elif observed_state == '1':
                for widget in widgets_a:
                    self.m_screen('home_mat').widgets[widget].toggle_state = 0
                    self.m_screen('home_mat').widgets[widget].toggle_widget(0)
                for widget in widgets_b:
                    self.m_screen('home_mat').widgets[widget].toggle_state = 1
                    self.m_screen('home_mat').widgets[widget].toggle_widget(1)

    def update_excel_selection(self):
        export_flag = ' [EXPORTED]' if self.exported else ''
        self.m_screen().widgets['xcl_input'].set_value('Entries in stored file: '
                                                       + str(len(DataHandler.export_entries))
                                                       + export_flag)

class DataHandler:
    job_type: int
    volume: float
    dimensions: Tuple[float, ...]
    export_entries = []
    tool = ''

    def __init__(self):
        self.data = dict(tool='',
                         job_type=-1,
                         dimensions=(0., 0., 0.),
                         block=(0., 0., 0.),
                         precision=0,
                         volume=0.,
                         hours=0.,
                         cost=0.,
                         cost_mat=0.,
                         cost_cut=0.,
                         units='inch',
                         conversion=1.,
                         additionals=None)

    def set_tool(self, tool):
        self.data['tool'] = DataHandler.tool = tool

    def set_dimensions(self, dimensions: Tuple[float, float, float]):
        self.data['dimensions'] = dimensions
        print("VAR DIMENSIONS SET TO", dimensions)

    def set_block(self, block: Tuple[float, float, float]):
        self.data['block'] = block

    def set_type(self, index):
        self.data['job_type'] = index
        # self.job_type = index

    def set_conversion(self, unit):
        self.data['unit'] = unit
        if unit == UNIT_TYPES[1]:
            self.data['conversion'] = 1 / 25.4
            # self.conversion = 1 / 25.4
        else:
            self.data['conversion'] = 1.
            # self.conversion = 1.

    def set_volume(self, volume):
        self.data['volume'] = float(volume)

    def set_additionals(self, values):
        self.data['additionals'] = values

    def set_cost(self, cost, mode=''):
        mode = '_' + mode if mode != '' else mode
        self.data['cost'+mode] = float(str(cost) + '0')

    def set_precision(self, precision):
        self.data['precision'] = float(precision)

    def set_combo(self, combo):
        self.data['combo'] = combo

    def set_hours(self, hours):
        self.data['hours'] = hours

    def get_hours(self):
        return self.data['hours']

    def get_combo(self):
        return self.data['combo']

    def get_precision(self):
        return self.data['precision']

    def get_dimensions(self):
        return self.data['dimensions']

    def get_block(self):
        return self.data['block']

    def get_type(self):
        return self.data['job_type']

    def get_conversion(self):
        return self.data['conversion']

    def get_tool(self):
        return DataHandler.tool if self.data['tool'] == '' else self.data['tool']

    def get_volume(self):
        return self.data['volume']

    def get_cost(self, mode=''):
        mode = '_' + mode if mode != '' else ''
        return self.data['cost' + mode]

    def get_data(self, mode):
        print(*[n for n in self.get_block()])
        if mode == 'mat':
            print("EXPORT DATA:\n", [self.get_tool(),
                    self.get_type(),
                    self.get_combo(),
                    *[n for n in self.get_dimensions()],
                    self.get_conversion(),
                    self.get_precision(),
                    *[n for n in self.get_block()],
                    self.get_volume(),
                    self.get_cost()])
            return [self.get_tool(),
                    self.get_type(),
                    self.get_combo(),
                    *[n for n in self.get_dimensions()],
                    self.get_conversion(),
                    self.get_precision(),
                    *[n for n in self.get_block()],
                    self.get_volume(),
                    self.get_hours(),
                    self.get_cost('mat'),
                    self.get_cost('cut'),
                    self.get_cost()]
        elif mode == 'cut':
            return (self.data['tool'],
                    self.data['job_type'],
                    *[n for n in self.data['dimensions']],
                    self.data['volume'],
                    self.data['precision'],
                    *[n for n in self.data['additionals']],
                    self.data['cost'])

    @staticmethod
    def add_entry(entry):
        DataHandler.export_entries.append(entry)

    @staticmethod
    def get_entries():
        return DataHandler.export_entries

    @staticmethod
    def reset_entries():
        DataHandler.export_entries = []


if __name__ == '__main__':
    Master()
