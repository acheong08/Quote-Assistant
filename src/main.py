from src.application import App
from src.application.utils import *
from src.application.gui import *
from src.pttech.constants import *


# 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

class Master(App):
    selected_input: StringVar

    def __init__(self):
        self.running = True

        home = ScreenUtil('Home',
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

        # export = ScreenUtil('Export',
        #                     file_button=[ButtonCustom(self.update_csv, w=10, content='Update CSV file'), 0.5, 0.5],
        #                     result_label=[LabelCustom(), 0.5, 0.75],
        #                     home_screen=[ButtonCustom(self.set_home, w=5, content='[Home]'), 0.5, 0.9])
        #
        # config = ScreenUtil('Config',
        #                     reset_button=[ButtonCustom(self.reset_json, w=10, content='Reset Json file'), 0.5, 0.5],
        #                     auto_button=[CheckbuttonCustom('Auto mode'), 0.5, 0.7],
        #                     home_screen=[ButtonCustom(self.set_home, w=5, content='[Home]'), 0.5, 0.9])

        # self.automated_process()

        super().__init__(title='Quote Assistant',
                         dimensions=(1500, 1000),
                         lock=False,
                         screens=[home()])

        self.running = False

    def set_config(self):
        pass

    def set_export(self):
        pass


if __name__ == '__main__':
    Master()
