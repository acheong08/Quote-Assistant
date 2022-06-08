import numpy
import openpyxl as pyxl
from typing import Tuple

from application import App
from application.utils import *
from application.gui import *
from pttech.constants import *


# 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

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
                          ms_header=[LabelCustom('PT TECH QUOTE ASSISTANT', font_size=50), 0.5, 0.05],
                          dt_header=[LabelCustom('Quote Details', font_size=36), 0.25, 0.2],
                          qte_label=[LabelCustom('Quote'), 0.15, 0.3],
                          qte_input=[InputCustom(), 0.35, 0.3],
                          typ_label=[LabelCustom('Job Type'), 0.15, 0.4],
                          typ_input=[OptionMenuCustom(''), 0.35, 0.4],
                          prc_label=[LabelCustom('Precision Level'), 0.15, 0.5],
                          prc_input=[OptionMenuCustom(*[str(n) for n in range(1, DIFFICULTIES + 1)]), 0.35, 0.5],
                          cf_button=[ButtonCustom(self.set_config, 'Config', 10, 2), 0.25, 0.9],
                          io_header=[LabelCustom('Input & Output', font_size=36), 0.75, 0.2],
                          dim_radio=[RadioButtonsCustom('Excel File', 'Manual input'), 0.75, 0.3],
                          xp_button=[ButtonCustom(self.set_export(), 'Export', 10, 2), 0.75, 0.9])

        export = ScreenUtil('Export',
                            exp_label=[LabelCustom(),
                                       0.5, 0.75],
                            rt_button=[ButtonCustom(self.return_home, 'Return', 10, 2),
                                       0.25, 0.9],
                            rs_button=[ButtonCustom(self.reset_home, 'Reset', 10, 2),
                                       0.75, 0.9])

        config = ScreenUtil('Config',
                            auto_button=[CheckbuttonCustom('Auto mode'),
                                         0.5, 0.7],
                            home_screen=[ButtonCustom(self.set_home, 'Return', 10, 2),
                                         0.5, 0.9])

        self.m_excel = ExcelIO()

        super().__init__(title='Quote Assistant',
                         dimensions=(1250, 750),
                         lock=False,
                         screens=[home(), export(), config()])

    def periodic(self):
        self.check_input_selection()

    def save_data_excel(self, path):
        self.m_excel.set_file(path)
        self.m_excel.get_data()

    def set_config(self):
        self.m_screen('Config').set_screen()

    def return_home(self):
        self.set_home()

    def reset_home(self):
        self.set_home()

    def set_home(self):
        self.m_screen('Home').set_screen()

    def set_export(self):
        print(self.m_screen('Home').widgets['dim_radio'].get_selection())
        self.m_screen('Export').set_screen()

    def check_input_selection(self):
        observed_state = self.m_screen('Home').widgets['dim_radio'].get_selection()
        previous_state = self.m_screen('Home').widgets['dim_radio'].previous_state
        if observed_state != previous_state:
            self.m_screen('Home').widgets['dim_radio'].previous_state = observed_state
            if observed_state == '0':
                self.m_screen('Home').widgets['fl_button'].toggle_widget(1)
                self.m_screen('Home').widgets['dmx_label'].toggle_widget(0)
                self.m_screen('Home').widgets['dmy_label'].toggle_widget(0)
                self.m_screen('Home').widgets['dmz_label'].toggle_widget(0)
                self.m_screen('Home').widgets['dmx_input'].toggle_widget(0)
                self.m_screen('Home').widgets['dmy_input'].toggle_widget(0)
                self.m_screen('Home').widgets['dmz_input'].toggle_widget(0)
            elif observed_state == '1':
                self.m_screen('Home').widgets['fl_button'].toggle_widget(0)
                self.m_screen('Home').widgets['dmx_label'].toggle_widget(1)
                self.m_screen('Home').widgets['dmy_label'].toggle_widget(1)
                self.m_screen('Home').widgets['dmz_label'].toggle_widget(1)
                self.m_screen('Home').widgets['dmx_input'].toggle_widget(1)
                self.m_screen('Home').widgets['dmy_input'].toggle_widget(1)
                self.m_screen('Home').widgets['dmz_input'].toggle_widget(1)


class DataHandler:

    def __init__(self):
        self.dimensions = (0, 0, 0)
        self.volume = 0

    def set_dimensions(self, dimensions: Tuple[float]):
        self.dimensions = dimensions
        self.volume = numpy.prod(self.dimensions)


class ExcelIO(BaseFileIO):

    def __init__(self):
        super().__init__()
        self.book = ...
        self.sheet = ...

    def set_file(self, file_path):
        super().set_file(file_path)
        self.book = pyxl.load_workbook(self.file_path)
        self.sheet = self.book[self.book.sheetnames[0]]

    # def find_cell(self):

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

    def extract_data(self, cells):
        for n in cells:
            pass


    def get_data(self):
        data = (0, 0, 0)
        mapping = ('')
        # for


if __name__ == '__main__':
    Master()
