#!/usr/bin/env python3
from typing import Tuple

from application import App
from application.utils import *
from application.gui import *
from pttech.constants import *

from pttech.calculations import *


class Master(App):
    selected_input: StringVar
    placeholder_excel_devpath = '../resources/documents/placeholder.xlsx'
    config_json_devpath = '../resources/documents/config.json'

    def __init__(self):
        menu = ScreenUtil('menu',
                          ms_header=[LabelCustom('PT TECH UTILITY', fg_color=MASTER_THEME['fgh'], font_size=50),
                                     0.5, 0.05],
                          mod_label=[LabelCustom('Select Mode'),
                                     0.5, 0.4],
                          mod_input=[OptionMenuCustom(*APP_MODES, w=25),
                                     0.5, 0.5])
        home_mat = ScreenUtil('home_mat',
                              ms_header=[LabelCustom('PT TECH UTILITY', fg_color=MASTER_THEME['fgh'], font_size=50),
                                         0.5, 0.05],
                              dt_header=[LabelCustom('Quote Details', fg_color=MASTER_THEME['fgh'], font_size=36),
                                         0.25, 0.2],
                              qte_label=[LabelCustom('Quote'),
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
                              cf_button=[ButtonCustom(self.set_config, 'Config', 20, 1, 'white', 'black'),
                                         0.25, 0.65],
                              mn_button=[ButtonCustom(self.reset_menu, 'Back to\nMenu', 10, 2),
                                         0.25, 0.9],
                              io_header=[LabelCustom('Input & Output', fg_color=MASTER_THEME['fgh'], font_size=36),
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

        export_mat = ScreenUtil('export_mat',
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

        config_mat = ScreenUtil('config_mat',
                                scs_label=[LabelCustom('Steel Cost per unit mass'),
                                           0.25, 0.1],
                                scs_input=[InputCustom(),
                                           0.75, 0.1],
                                zcs_label=[LabelCustom('Zinc Cost per unit mass'),
                                           0.25, 0.2],
                                zcs_input=[InputCustom(),
                                           0.75, 0.2],
                                acs_label=[LabelCustom('Aluminum Cost per unit mass'),
                                           0.25, 0.3],
                                acs_input=[InputCustom(),
                                           0.75, 0.3],
                                rt_button=[ButtonCustom(self.update_config, 'Update', 10, 2),
                                           0.5, 0.9])

        # TODO: set positions of widgets
        home_mac = ScreenUtil('home_mac',
                              job_label=[LabelCustom("Quote"),
                                         0.4, 0.2],
                              job_input=[InputCustom(),
                                         0.6, 0.2],
                              mat_label=[LabelCustom("Material"),
                                         0.4, 0.3],
                              mat_input=[InputCustom(),
                                         0.6, 0.3],
                              prc_label=[LabelCustom("Precision"),
                                         0.4, 0.4],
                              prc_input=[OptionMenuCustom(*DIFFICULTIES),
                                         0.6, 0.4],
                              fil_label=[LabelCustom("Input File"),
                                         0.4, 0.5],
                              fl_button=[FileButtonCustom(self.set_export),
                                         0.6, 0.5],
                              mn_button=[ButtonCustom(self.reset_menu, 'Back to\nMenu', 10, 2),
                                         0.25, 0.9],
                              )

        self.m_import = ExcelIO()
        self.m_export = ExcelIO()
        self.m_config = JsonIO()
        self.m_data = DataHandler()
        self.m_calc = MasterCalculations()

        self.m_config.set_file(Master.config_json_devpath)

        assert isinstance(self.m_calc(Material), Material)

        super().__init__(title='Quote Assistant',
                         dimensions=(1250, 750),
                         lock=True,
                         screens=[menu(), home_mat(), export_mat(), config_mat()])

    def periodic(self):
        self.check_screen_selection() if self.m_screen.current_screen == self.m_screen('menu') else None
        self.check_input_selection() if self.m_screen.current_screen == self.m_screen('home_mat') else None

    def reset_menu(self):
        self.m_screen('menu').reset_screen()

    def save_data_excel(self, path):
        self.m_import.set_file(path)
        self.m_import.extract_data(CIMATRON_LOCATORS)
        self.m_data.set_dimensions(tuple(self.m_import.get_data()))

    def save_data_manual(self):
        # noinspection PyTypeChecker
        self.m_data.set_dimensions(tuple([float(self.m_screen().widgets[str('dm' + n + '_input')].get_value(float))
                                          for n in ('x', 'y', 'z')]))

    def set_config(self):
        data = self.m_config.get_entries()
        self.m_screen('config_mat').widgets['scs_input'].set_value(data['cost_per_pound_steel'])
        self.m_screen('config_mat').widgets['zcs_input'].set_value(data['cost_per_pound_zinc'])
        self.m_screen('config_mat').widgets['acs_input'].set_value(data['cost_per_pound_aluminum'])
        self.m_screen('config_mat').set_screen()

    def update_config(self):
        self.m_config.edit_entry('cost_per_pound_steel',
                                 self.m_screen('config_mat').widgets['scs_input'].get_value(float))
        self.m_config.edit_entry('cost_per_pound_zinc',
                                 self.m_screen('config_mat').widgets['zcs_input'].get_value(float))
        self.reset_home()

    def return_home(self):
        self.m_data = DataHandler()
        self.m_calc = MasterCalculations()
        self.set_home()

    def reset_home(self):
        self.m_data = DataHandler()
        self.m_calc = MasterCalculations()
        self.m_screen('home_mat').reset_screen()

    def set_home(self):
        self.m_screen('home_mat').set_screen()

    def set_export(self):
        if not self.process_data():
            return
        self.m_screen('export_mat').widgets['exp_label'].set_value('Total Volume: ' + str(round(self.m_calc(
                Material).required_volume, 2)))
        self.m_screen('export_mat').widgets['cst_label'].set_value('Total cost: ~$' + str(round(self.m_calc(
                Material).get_cost(), 2)))
        self.m_screen('export_mat').set_screen()

    def process_data(self):
        if sum(self.m_data.get_dimensions()) <= 0:
            self.save_data_manual()
        try:
            self.m_data.set_type(self.m_screen().widgets['typ_input'].get_value())
            self.m_data.set_type(self.m_screen().widgets['typ_input'].get_value())
            self.m_data.set_conversion(self.m_screen().widgets['msm_input'].get_value())
            self.m_data.set_quote(self.m_screen().widgets['qte_input'].get_value())
            self.m_data.set_precision(self.m_screen().widgets['prc_input'].get_value())
            print("GOT JOB TYPE:", self.m_data.get_type())
            print("GOT DATA TYPE:", self.m_data.get_conversion())
            self.m_calc(Material).calculate_cost(QUOTE_TYPES.index(self.m_data.get_type()),
                                                 self.m_data.get_dimensions(),
                                                 self.m_data.get_conversion(),
                                                 self.m_data.get_precision(),
                                                 self.m_config.get_entries())
        except ValueError:
            self.m_error.display('Not all fields are filled out correctly!\nPlease try again.')
            return False
        self.m_data.set_volume(round(self.m_calc(Material).get_volume(), 2))
        self.m_data.set_cost(round(self.m_calc(Material).get_cost(), 2))
        return True

    def append_data(self):
        self.m_data.add_entry(self.m_data.get_data())
        print("-ADDED ENTRY")

    def export_data(self):
        from datetime import datetime as dt
        from pathlib import Path as pt

        # self.append_data()

        entries = self.m_data.get_entries()
        quote_info = self.m_data.get_quote() if len(entries) == 1 else "Quotes"
        self.m_export.create_file(Master.placeholder_excel_devpath,
                                  str(pt.home()
                                      / 'Downloads'
                                      / str(
                                          '[' + quote_info + '] '
                                          + dt.now().strftime(" %Y-%m-%d  ""%H-%M-%S")
                                          + '.xlsx')))
        for index, entry in enumerate(entries):
            self.m_export.manipulate_file(entry, index + 3)
        print("-EXPORTED ALL ENTRIES")

    def reset_data(self):
        self.m_data.reset_entries()

    def check_screen_selection(self):
        observed_state = self.m_screen('menu').widgets['mod_input'].get_value()
        self.m_screen('home_mat').reset_screen() if observed_state == 'Material Costs' else None

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


class DataHandler:
    job_type: int
    volume: float
    dimensions: Tuple[float, ...]
    export_entries = []
    quote = ''

    def __init__(self):
        self.data = dict(quote='',
                         job_type=-1,
                         dimensions=(0., 0., 0.),
                         precision=0,
                         volume=0.,
                         cost=0.,
                         conversion=1.)

    def set_quote(self, quote):
        self.data['quote'], DataHandler.quote = quote


    def set_dimensions(self, dimensions: Tuple[float, float, float]):
        self.data['dimensions'] = dimensions
        # self.dimensions = dimensions
        # self.volume = float(numpy.prod(self.dimensions))

    def set_type(self, index):
        self.data['job_type'] = index
        # self.job_type = index

    def set_conversion(self, unit):
        if unit == UNIT_TYPES[1]:
            self.data['conversion'] = 1 / 25.4
            # self.conversion = 1 / 25.4
        else:
            self.data['conversion'] = 1.
            # self.conversion = 1.

    def set_volume(self, volume):
        self.data['volume'] = float(volume)

    def set_cost(self, cost):
        self.data['cost'] = float(str(cost) + '0')

    def set_precision(self, precision):
        self.data['precision'] = float(precision)

    def get_precision(self):
        return self.data['precision']

    def get_dimensions(self):
        return self.data['dimensions']

    def get_type(self):
        return self.data['job_type']

    def get_conversion(self):
        return self.data['conversion']

    def get_quote(self):
        return DataHandler.quote if self.data['quote'] == '' else self.data['quote']

    def get_volume(self):
        return self.data['volume']

    def get_cost(self):
        return self.data['cost']

    def get_data(self):
        return (self.data['quote'],
                self.data['job_type'],
                *[n for n in self.data['dimensions']],
                self.data['precision'],
                self.data['volume'],
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
