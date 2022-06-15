#!/usr/bin/env python3
import _io
import shutil
import time

import numpy
import openpyxl as pyxl
from typing import Tuple, IO

from application import App
from application.utils import *
from application.gui import *
from pttech.constants import *

# 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
from src.pttech.calculations import *


class Master(App):
    selected_input: StringVar

    def __init__(self):
        home = ScreenUtil('Home',
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
                          cf_button=[ButtonCustom(self.set_config, 'Config', 10, 2),
                                     0.25, 0.9],
                          io_header=[LabelCustom('Input & Output', fg_color=MASTER_THEME['fgh'], font_size=36),
                                     0.75, 0.2],
                          dim_radio=[RadioButtonsCustom('Excel File', 'Manual input'),
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

        export = ScreenUtil('Export',
                            exp_label=[LabelCustom(),
                                       0.5, 0.4],
                            cst_label=[LabelCustom(),
                                       0.5, 0.5],
                            xp_button=[ButtonCustom(self.export_data, 'Export', 10, 2),
                                       0.5, 0.9],
                            rt_button=[ButtonCustom(self.return_home, 'Return', 10, 2),
                                       0.25, 0.9],
                            rs_button=[ButtonCustom(self.reset_home, 'Reset', 10, 2),
                                       0.75, 0.9])

        config = ScreenUtil('Config',
                            auto_button=[CheckbuttonCustom('Auto mode'),
                                         0.5, 0.7],
                            home_screen=[ButtonCustom(self.reset_home, 'Return', 10, 2),
                                         0.5, 0.9])

        self.m_import = ExcelIO()
        self.m_export = ExcelIO()
        self.m_data = DataHandler()
        self.m_calc = MasterCalculations()

        assert isinstance(self.m_calc(Material), Material)

        super().__init__(title='Quote Assistant',
                         dimensions=(1250, 750),
                         lock=False,
                         screens=[home(), export(), config()])

    def periodic(self):
        self.check_input_selection() if self.m_screen.current_screen == self.m_screen('Home') else None

    def save_data_excel(self, path):
        self.m_import.set_file(path)
        self.m_import.extract_data(CIMATRON_LOCATORS)
        self.m_data.set_dimensions(tuple(self.m_import.get_data()))
        print(self.m_data.dimensions)

    def save_data_manual(self):
        # noinspection PyTypeChecker
        self.m_data.set_dimensions(tuple([float(self.m_screen().widgets[str('dm' + n + '_input')].get_value(float))
                                          for n in ('x', 'y', 'z')]))
        print(self.m_data.dimensions)

    def set_config(self):
        # self.m_screen().widgets['ms_header'].set_value('TEST')
        self.m_screen('Config').set_screen()

    def return_home(self):
        self.set_home()

    def reset_home(self):
        print("RESETTING HOME")
        self.m_data = DataHandler()
        self.m_screen('Home').reset_screen()

    def set_home(self):
        self.m_screen('Home').set_screen()

    def set_export(self):
        if self.process_data():
            print(self.m_screen().widgets['dim_radio'].get_selection())
        self.m_screen('Export').widgets['exp_label'].set_value('Total Volume: ' + str(round(self.m_calc(
            Material).required_volume, 2)))
        self.m_screen('Export').widgets['cst_label'].set_value('Total cost: ~$' + str(round(self.m_calc(
            Material).get_cost(), 2)))
        self.m_screen('Export').set_screen()

    def process_data(self):
        if sum(self.m_data.get_dimensions()) <= 0:
            self.save_data_manual()
        self.m_data.set_type(self.m_screen().widgets['typ_input'].get_value())
        self.m_data.set_type(self.m_screen().widgets['typ_input'].get_value())
        self.m_data.set_conversion(self.m_screen().widgets['msm_input'].get_value())
        self.m_data.set_quote(self.m_screen('Home').widgets['qte_input'].get_value())
        print("GOT JOB TYPE:", self.m_data.get_type())
        print("GOT DATA TYPE:", self.m_data.get_conversion())
        self.m_calc(Material).calculate_cost(QUOTE_TYPES.index(self.m_data.get_type()),
                                             self.m_data.get_dimensions(),
                                             self.m_data.get_conversion())
        self.m_data.set_volume(round(self.m_calc(Material).get_volume(), 2))
        self.m_data.set_cost(round(self.m_calc(Material).get_cost(), 2))
        return True

    def export_data(self):
        from datetime import datetime as dt
        from pathlib import Path as pt

        current_dt = dt.now().strftime(" %Y-%m-%d_%H-%M-%S")
        file_path = str(
            pt.home() / 'Downloads' / str('[' + self.m_data.get_quote()
                                          + '] ' + current_dt
                                          + '.xlsx'))
        self.m_export.create_file('../resources/documents/placeholder.xlsx', file_path)
        self.m_export.manipulate_file(self.m_data.get_data(), 3)

    def check_input_selection(self):
        widgets_a = ['fl_button']
        widgets_b = ['dmx_label', 'dmy_label', 'dmz_label', 'dmx_input', 'dmy_input', 'dmz_input']
        observed_state = self.m_screen('Home').widgets['dim_radio'].get_selection()
        previous_state = self.m_screen('Home').widgets['dim_radio'].previous_state
        if observed_state != previous_state:
            self.m_screen('Home').widgets['dim_radio'].previous_state = observed_state
            if observed_state == '0':
                for widget in widgets_a:
                    self.m_screen('Home').widgets[widget].toggle_state = 1
                    self.m_screen('Home').widgets[widget].toggle_widget(1)
                for widget in widgets_b:
                    self.m_screen('Home').widgets[widget].toggle_state = 0
                    self.m_screen('Home').widgets[widget].toggle_widget(0)
            elif observed_state == '1':
                for widget in widgets_a:
                    self.m_screen('Home').widgets[widget].toggle_state = 0
                    self.m_screen('Home').widgets[widget].toggle_widget(0)
                for widget in widgets_b:
                    self.m_screen('Home').widgets[widget].toggle_state = 1
                    self.m_screen('Home').widgets[widget].toggle_widget(1)


class DataHandler:
    job_type: int
    volume: float
    dimensions: Tuple[float, ...]

    def __init__(self):
        self.dimensions = (0., 0., 0.)
        self.volume = 0.
        self.job_type = -1
        self.conversion = 1

        self.data = dict(quote='',
                         job_type=-1,
                         dimensions=(0., 0., 0.),
                         precision=0,
                         volume=0.,
                         cost=0.,
                         conversion=1.)

    def set_quote(self, quote):
        self.data['quote'] = quote

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
        self.data['volume'] = volume

    def set_cost(self, cost):
        self.data['cost'] = cost

    def get_dimensions(self):
        return self.data['dimensions']

    def get_type(self):
        return self.data['job_type']

    def get_conversion(self):
        return self.data['conversion']

    def get_quote(self):
        return self.data['quote']

    def get_volume(self):
        return self.data['volume']

    def get_cost(self):
        return self.data['cost']

    def get_data(self):
        # print((self.data['quote'],
        #         self.data['job_type'],
        #         *[[n] for n in self.data['dimensions']],
        #         self.data['precision'],
        #         self.data['volume'],
        #         self.data['cost']))
        return (self.data['quote'],
                self.data['job_type'],
                *[n for n in self.data['dimensions']],
                self.data['precision'],
                self.data['volume'],
                self.data['cost'])


class ExcelIO(BaseFileIO):

    def __init__(self):
        super().__init__()
        self.book = ...
        self.sheet = ...

    def set_file(self, file_path):
        super().set_file(file_path)
        self.book = pyxl.load_workbook(self.file_path)
        self.sheet = self.book[self.book.sheetnames[0]]

    def create_file(self, src, dst):
        shutil.copy(src, dst)
        time.sleep(1)
        self.set_file(dst)

    @staticmethod
    def get_cell(x, y, letter=''):
        alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                    'U', 'V', 'W', 'X', 'Y', 'Z']

        while x >= 1:
            if x <= 26:
                letter += alphabet[x - 1]
                x = 0
            else:
                letter += alphabet[int(x) // 26 - 1]
                x %= 26
        return letter + str(y)

    def manipulate_file(self, data, row=1, column=1):
        for index, item in enumerate(data):
            print(type(self.sheet[self.get_cell(index + column, row)]), item)
            self.sheet[self.get_cell(index + column, row)].value = item
        self.book.save(self.file_path)

    def extract_data(self, cells):
        for n, cell in enumerate(cells):
            print("SEARCHING FOR", cell)
            for r in range(1, 100):
                value = self.sheet[self.get_cell(1, r)].value
                print(value)
                if value == cell:
                    self.data.append(float(self.sheet[self.get_cell(2, r)].value))
                    print("FOUND")
            if len(self.data) < n:
                print("NOT FOUND.")
        print("DONE:", self.data)


if __name__ == '__main__':
    Master()
