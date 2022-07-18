#!/usr/bin/env python3

"""
HOW TO EXPORT TO EXE:
1. Go to the terminal tab
2. Set current directory to /output
3. Run the command 'pyinstaller main.spec'
"""

from application import App

from application.utils import *
from application.gui import *

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
        # Setting the geometry possibilities of each window
        self.default_geometry = (500, 500)
        self.large_geometry = (1250, 750)
        self.medium_geometry = (1000, 750)
        # Menu screen GUI (currently unused)
        # menu = ScreenUtil('menu', self.default_geometry,
        #                   ms_header=[LabelCustom('PT TECH UTILITY', fg_color=MASTER_THEME['fgh'], font_size=50, w=15,
        #                                          height=2),
        #                              0.5, 0.1],
        #                   mod_label=[LabelCustom('Select Mode'),
        #                              0.5, 0.4],
        #                   mod_input=[OptionMenuCustom(*APP_MODES, w=25),
        #                              0.5, 0.5])

        # Material home screen GUI
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

        # Material export screen GUI
        export_mat = ScreenUtil('export_mat', self.large_geometry,
                                # md_header=[OptionMenuCustom(*APP_MODES, w=21, font_size=8, default_text=''),
                                #            0.9, 0.05],
                                exp_label=[LabelCustom(w=50),
                                           0.5, 0.1],
                                cs1_label=[LabelCustom(w=50),
                                           0.5, 0.2],
                                cs2_label=[LabelCustom(w=50),
                                           0.5, 0.3],
                                cst_label=[LabelCustom(w=50),
                                           0.5, 0.4],
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

        # Material config screen GUI
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
                                ud_button=[ButtonCustom(self.update_config, 'Update', 10, 2),
                                           0.5, 0.9],
                                rt_button=[ButtonCustom(self.reset_home, 'Cancel', 7, 1),
                                           0.9, 0.9])

        # Cutting home screen GUI
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

        # Cutting export screen GUI
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

        # Initializing custom file input/outputs required for this application
        self.m_import = ExcelIO()
        self.m_export = ExcelIO()
        self.m_config = JsonIO()

        # Initializing data and calculation managers
        self.m_data = Master.DataHandler()
        self.m_calc = MasterCalculations()

        # Setting config file path
        self.m_config.set_file(Master.config_json_devpath)

        # Exported variable handles whether export button has immediately been pressed
        self.exported = False

        # Ignore
        assert isinstance(self.m_calc(Material), Material)
        assert isinstance(self.m_calc(Cutting), Cutting)

        # Calling the super class application with all custom modifications and screens
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
        """
        Overridden method that loops every 10-20ms or so in the superclass
        """

        self.check_input_selection() if self.m_screen.current_screen is self.m_screen('home_mat') else \
            self.update_excel_selection() if self.m_screen.current_screen is self.m_screen('export_mat') else None

    def get_mode(self, shorthand=False):
        """
        Method that returns the mode that the application is in. Currently there is only support for material mode;
        cutting is not yet configured.

        @param shorthand: whether to return the three letter shorthand as opposed to the full mode name
        """
        for n, mode in enumerate(APP_MODES):
            if self.m_screen().get_name()[-3:] in mode.lower():
                return APP_MODES[n] if not shorthand else self.m_screen().get_name()[-3:]
        return self.m_screen().get_name()

    def reset_menu(self):
        """
        Method that re-initializes then sets the screen to menu page (currently unused)
        """
        self.m_screen('menu').reset_screen()
        self.window.geometry('500x500')

    def save_data_excel(self, path):
        """
        Method that extracts data from a Cimatron excel file inputted by the user.

        @param path: file location path
        """
        # Import handler file set
        self.m_import.set_file(path)
        print(self.m_screen().get_name())
        # Excel file IO handler extracts the relevant information in accordance to the preset Cimatron locator
        self.m_import.extract_data(CIMATRON_LOCATORS[self.m_screen().get_name()[-3:]], offset=(1, 0))
        # Dimensions, now extracted from excel file are imported into the data storage class
        self.m_data.set_dimensions(tuple(self.m_import.get_data()[:3]))
        # Currently useless
        if self.get_mode() == APP_MODES[1]:
            self.m_data.set_volume(self.m_import.get_data()[3])

        print(self.m_data.get_dimensions(), '|', self.m_data.get_volume())

    # noinspection PyTypeChecker
    def save_data_manual(self):
        """
        Method that extracts the values from the input widgets assigned to the box_dimensions if option is selected.
        """
        self.m_data.set_dimensions(tuple([float(self.m_screen().widgets[str('dm' + n + '_input')].get_value(float))
                                          for n in ('x', 'y', 'z')]))

    def set_config(self):
        """
        Method that sets retrieves configuration values and displays them.
        """

        # Data is retrieved from the config entries
        data = self.m_config.get_entries()
        # Values of inputs assigned to matching values in config
        self.m_screen('config_mat').widgets['sc1_input'].set_value(data['cost_per_pound_steel'])
        self.m_screen('config_mat').widgets['zc1_input'].set_value(data['cost_per_pound_zinc'])
        self.m_screen('config_mat').widgets['ac1_input'].set_value(data['cost_per_pound_aluminum'])
        self.m_screen('config_mat').widgets['sc2_input'].set_value(data['cost_per_hour_steel'])
        self.m_screen('config_mat').widgets['zc2_input'].set_value(data['cost_per_hour_zinc'])
        self.m_screen('config_mat').widgets['ac2_input'].set_value(data['cost_per_hour_aluminum'])
        # Home removed, config widgets displayed
        self.m_screen('config_mat').set_screen()

    def update_config(self):
        """
        Method to update config based on changed values on the config screen.
        """
        try:
            self.m_config.edit_entry('cost_per_pound_steel',
                                     float(self.m_screen('config_mat').widgets['sc1_input'].get_value(float)))
            self.m_config.edit_entry('cost_per_pound_zinc',
                                     float(self.m_screen('config_mat').widgets['zc1_input'].get_value(float)))
            self.m_config.edit_entry('cost_per_pound_aluminum',
                                     float(self.m_screen('config_mat').widgets['ac1_input'].get_value(float)))
            self.m_config.edit_entry('cost_per_hour_steel',
                                     float(self.m_screen('config_mat').widgets['sc2_input'].get_value(float)))
            self.m_config.edit_entry('cost_per_hour_zinc',
                                     float(self.m_screen('config_mat').widgets['zc2_input'].get_value(float)))
            self.m_config.edit_entry('cost_per_hour_aluminum',
                                     float(self.m_screen('config_mat').widgets['ac2_input'].get_value(float)))
        except ValueError:
            self.m_error.display('Not all fields have been inputted properly.')
            return

        self.reset_home()

    def return_home(self):
        """
        Method that switches screen back to home, but does NOT reset it.
        """
        self.m_calc = MasterCalculations()
        self.m_screen('home_' + self.get_mode(True)).set_screen()

    def reset_home(self):
        """
        Method that switches AND resets screen back to home.
        """

        # Data storage and calculator both re-initialized
        self.m_data = Master.DataHandler()
        self.m_calc = MasterCalculations()
        print(self.get_mode(True))
        # Home screen reset
        self.m_screen('home_' + self.get_mode(True)).reset_screen()

    def set_export(self):
        """
        Method that attempts to verify inputs, and then switches the screen to export.
        """

        # Stops execution of the following lines if data is not processed properly
        if not self.process_data():
            return
        # Verifies the application is in materials mode
        if self.get_mode() == APP_MODES[0]:
            # Various widgets on the export screen are configured in accordance with the now-processed ata
            self.m_screen('export_mat').widgets['exp_label'].set_value('Total Volume: ' + str(round(self.m_calc(
                    Material).required_volume, 2)))
            self.m_screen('export_mat').widgets['cs1_label'].set_value('Total Material Cost: ~$'
                                                                       + str(round(self.m_data.get_cost('mat'), 2)))
            self.m_screen('export_mat').widgets['cs2_label'].set_value('Total Cutting Cost (rough): ~$'
                                                                       + str(round(self.m_data.get_cost('cut'), 2)))
            self.m_screen('export_mat').widgets['cst_label'].set_value('Total Combined Cost (very rough): ~$'
                                                                       + str(round(self.m_data.get_cost(), 2)))
            # Reset exported variable to false
            self.exported = False
            # Set screen to export
            self.m_screen('export_mat').set_screen()
        # Currently unused
        elif self.get_mode() == APP_MODES[1]:
            self.m_screen('export_cut').widgets['cst_label'].set_value('Total cost in hours: ~' + str(self.m_calc(
                    Cutting).get_cost()))
            self.m_screen('export_cut').set_screen()

    def process_data(self):
        """
        Method that attempts to store and process input and output data.

        @return: boolean concerning whether or not inputs have been validated
        """

        # Try-except structure to catch
        try:
            if not self.m_screen().widgets['fl_button'].is_file_inputted():
                self.save_data_manual()
            print("---MODE: ", self.get_mode())
            self._process_mat_calc() if self.get_mode() == APP_MODES[0] else self._process_cut_calc() if \
                self.get_mode() == APP_MODES[1] else None
        except (ValueError, KeyError) as ex:
            self.m_error.display('Not all fields are filled out correctly!\nPlease try again.', ex)
            return False
        self._export_mat_calc() if self.get_mode() == APP_MODES[0] \
            else self._export_cut_calc() if self.get_mode() == APP_MODES[1] \
            else None
        return True

    def _process_mat_calc(self):
        """
        Internal method to process material information specifically (now includes cutting hours testing).
        """

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

        # Material calculator calculates cost with the parameters just
        print("--ATTEMPTING: Calculation")
        self.m_calc(Material).calculate_cost(QUOTE_TYPES.index(self.m_data.get_type()),
                                             self.m_data.get_dimensions(),
                                             self.m_data.get_conversion(),
                                             self.m_data.get_precision(),
                                             self.m_data.get_combo(),
                                             self.m_config.get_entries())
        self.m_data.set_volume(round(self.m_calc(Material).get_volume(), 2))
        self.m_data.set_block(self.m_calc(Material).get_block())
        print("WTF IS THE VOLUME:", self.m_data.get_volume())
        self.m_calc(Cutting).calculate_cost(QUOTE_TYPES.index(self.m_data.get_type()),
                                            self.m_data.get_block(),
                                            self.m_data.get_dimensions(),
                                            self.m_data.get_precision(),
                                            self.m_data.get_conversion(True),
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
        """
        Internal method that sets appropropriate values post-calculation into their corresponding values in the
        dictionary found within the data storage.
        """
        self.m_data.set_cost(round(self.m_calc(Material).get_cost(), 2), 'mat')
        self.m_data.set_cost(round(self.m_calc(Cutting).get_cost(), 2), 'cut')
        self.m_data.set_cost(round(self.m_calc.get_cumulative_cost(), 2))

    def _export_cut_calc(self):
        self.m_data.set_additionals(self.m_calc(Cutting).get_additional_values)
        self.m_data.set_cost(self.m_calc(Cutting).get_cost())

    def append_data(self):
        """
        Method that adds an entry to a class variable to be exported to excel.
        """

        self.exported = False
        self.m_data.add_entry(self.m_data.get_data(self.get_mode(True)))
        print("-ADDED ENTRY")

    def export_data(self):
        """
        Method that exports said entry(s) in a variable as determined by the above method.
        """

        from datetime import datetime as dt
        from pathlib import Path as Pt

        # self.append_data()

        entries = self.m_data.get_entries()
        print("EXPORT ENTRIES:\n", entries)
        # The title of the document is configured so it is not blank
        quote_info = self.m_data.get_tool() if len(entries) == 1 and entries[0][0] != '' else "Quotes"
        # The placeholder file is determined (which type of base file to write on)
        file = Master.mat_placeholder_excel_devpath if self.get_mode() == APP_MODES[0] else \
            Master.cut_placeholder_excel_devpath if self.get_mode() == APP_MODES[1] else ''
        # A copy of the selected placeholder file is made in the user downloads folder
        self.m_export.create_file(file,
                                  str(Pt.home()
                                      / 'Downloads'
                                      / str(
                                          '[' + quote_info + '] '
                                          + dt.now().strftime(" %Y-%m-%d  ""%H-%M-%S")
                                          + '.xlsx')))
        # Enumeration through each item in the list of entries to append them to the excel spreadsheet
        for index, entry in enumerate(entries):
            self.m_export.manipulate_file(entry, index + 3)
        # Exported text will now display on the UI
        self.exported = True
        print("-EXPORTED ALL ENTRIES")

    def reset_data(self):
        """
        Method that resets the entries variable containing any previous entries added.
        """

        self.m_data.reset_entries()
        # Exported text will be hence removed from the UI
        self.exported = False

    def set_current_screen(self):
        """
        Method that switches screens based on the mode selection. Should be run periodically. Currently unused.
        """

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
            if self.m_screen.transitioning:
                continue
            elif search not in value and search not in screen:
                Master.flag = True
                continue
            elif search in value:
                if search in screen:
                    Master.flag = False
                    continue
                self.m_screen('home_' + search).reset_screen()
                for loc, item in enumerate(array):
                    if item in self.m_screen().get_name():
                        temp = modes[loc]
                        array.remove(item)
                        modes.pop(loc)
                        array.append(item)
                        modes.append(temp)
                Master.flag = True
                break
            elif search in screen and Master.flag:
                self.m_screen().widgets['md_header'].set_value(modes[index])
                break

    def check_screen_selection(self):
        observed_state = self.m_screen('menu').widgets['mod_input'].get_value()
        self.m_screen('home_mat').reset_screen() if observed_state == APP_MODES[0] else \
            self.m_screen('home_cut').reset_screen() if observed_state == APP_MODES[1] else None

    def check_input_selection(self):
        """
        Method to check which widgets to display corresponding to type of input selection. Should be run periodically.
        """

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
                                                       + str(len(Master.DataHandler.export_entries))
                                                       + export_flag)

    class DataHandler:
        """Class to handle the management of data storage for all inputs and outputs."""

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
            self.data['tool'] = Master.DataHandler.tool = tool

        def set_dimensions(self, dimensions: Tuple[float, float, float]):
            self.data['box_dimensions'] = dimensions
            print("VAR DIMENSIONS SET TO", dimensions)

        def set_block(self, block: Tuple[float, float, float]):
            self.data['block'] = block

        def set_type(self, index):
            self.data['job_type'] = index
            # self.job_type = index

        def set_conversion(self, unit):
            self.data['unit'] = unit
            self.data['conversion'] = 1 / 25.4 if unit == UNIT_TYPES[1] else 1.
            self.data['rev_conversion'] = 1. if unit == UNIT_TYPES[1] else 1 / 25.4

        def set_volume(self, volume):
            self.data['volume'] = float(volume)

        def set_additionals(self, values):
            self.data['additionals'] = values

        def set_cost(self, cost, mode=''):
            mode = '_' + mode if mode != '' else mode
            self.data['cost' + mode] = float(str(cost) + '0')

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
            return self.data['box_dimensions']

        def get_block(self):
            return self.data['block']

        def get_type(self):
            return self.data['job_type']

        def get_conversion(self, rev=False):
            return self.data['conversion'] if not rev else self.data['rev_conversion']

        def get_tool(self):
            return Master.DataHandler.tool if self.data['tool'] == '' else self.data['tool']

        def get_volume(self):
            return self.data['volume']

        def get_cost(self, mode=''):
            mode = '_' + mode if mode != '' else ''
            return self.data['cost' + mode]

        def get_unit(self):
            return self.data['unit']

        def get_data(self, mode):
            print(*[n for n in self.get_block()])
            if mode == 'mat':
                print("EXPORT DATA:\n", [self.get_tool(),
                                         self.get_type(),
                                         self.get_combo(),
                                         *[n for n in self.get_dimensions()],
                                         self.get_unit(),
                                         self.get_precision(),
                                         *[n for n in self.get_block()],
                                         self.get_volume(),
                                         self.get_cost()])
                return [self.get_tool(),
                        self.get_type(),
                        self.get_combo(),
                        *[n for n in self.get_dimensions()],
                        self.get_unit(),
                        self.get_precision(),
                        *[n for n in self.get_block()],
                        self.get_volume(),
                        self.get_hours(),
                        self.get_cost('mat'),
                        self.get_cost('cut'),
                        self.get_cost()]
            elif mode == 'cut':
                return [self.data['tool'],
                        self.data['job_type'],
                        *[n for n in self.data['box_dimensions']],
                        self.data['volume'],
                        self.data['precision'],
                        *[n for n in self.data['additionals']],
                        self.data['cost']]

        @staticmethod
        def add_entry(entry):
            Master.DataHandler.export_entries.append(entry)

        @staticmethod
        def get_entries():
            return Master.DataHandler.export_entries

        @staticmethod
        def reset_entries():
            Master.DataHandler.export_entries = []


if __name__ == '__main__':
    Master()
