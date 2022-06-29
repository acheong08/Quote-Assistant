import json
import os
import shutil
import time
import openpyxl as pyxl
from typing import Dict, Tuple

try:
    from application.gui import WidgetCustom
except ImportError:
    from src.application.gui import WidgetCustom


class ScreenUtil:
    # Dict[str, list[WidgetCustom, float, float]]
    def __init__(self, name: str, geometry: Tuple = None, **kwargs):
        self.name = name
        self.widgets = kwargs
        self.geometry = geometry
        self.screen = [self.name, self.geometry, self.widgets]
        print(self.screen)

    def __call__(self, index=-1, *args, **kwargs):
        return self.screen[index] if index > -1 else self.screen


class BaseFileIO:
    file_path: str
    data: list

    def __init__(self, file=..., file_path=''):
        self.file = file
        self.file_path = file_path
        self.data = []

        if file_path != '':
            try:
                self.set_file(self.file_path)
            except IOError:
                pass

    def set_file(self, file_path):
        self.file_path = str(file_path)
        self.file = open(str(self.file_path), 'a')

    def manipulate_file(self, *args):
        self.file.close()
        self.file = open(self.file_path, 'w')
        self.file.writelines(args)
        self.file.close()

    def get_data(self):
        return self.data

    def get_text(self):
        try:
            return self.file.read().splitlines()
        except ValueError:
            self.file = open(self.file_path, 'r')
            return self.file.read().splitlines()


class CsvFileIO(BaseFileIO):

    def __init__(self):
        super().__init__()

    # def editCsv(self):


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
            # print(type(self.sheet[self.get_cell(index + column, row)]), item)
            self.sheet[self.get_cell(index + column, row)].value = item
        self.book.save(self.file_path)

    def extract_data(self, cells, x_range=1, y_range=100, offset=(0, 0)):
        self.data = []
        for n, cell in enumerate(cells):
            print("SEARCHING FOR", cell)
            for c in range(1, x_range + 1):
                for r in range(1, y_range + 1):
                    value = self.sheet[self.get_cell(c, r)].value
                    print(c, r, value)
                    if value == cell:
                        self.data.append(float(self.sheet[self.get_cell(c + offset[0], r + offset[1])].value))
                        print("FOUND")
            if len(self.data) < n:
                print("NOT FOUND.")
        print("DONE:", self.data)


class JsonIO(BaseFileIO):

    def __init__(self):
        super().__init__()

    def add_entries(self, txt_input, fields):

        with open(self.file_path, 'r', encoding="utf-8", errors="replace") as self.file:
            self.data = json.load(self.file)

        for n, txt_input in enumerate(txt_input):
            entry = {}
            for index, key in enumerate(fields):
                entry[key] = txt_input[index]
            self.data.append(entry)

        self.file = open(self.file_path, 'w', encoding="utf-8", errors="replace")
        self.file.write(json.dumps(self.data, sort_keys=False, indent=4))
        self.file.close()

    def edit_entry(self, entry, value):
        self.file = open(self.file_path, 'w', encoding="utf-8", errors="replace")
        self.data[entry] = value
        self.file.write(json.dumps(self.data, sort_keys=False, indent=4))
        self.file.close()

    def write_entries(self):
        self.file = open(self.file_path, 'w', encoding="utf-8", errors="replace")
        self.file.write(json.dumps(self.data, sort_keys=False, indent=4))

    def clear_entries(self):
        with open(self.file_path, 'w', encoding="utf-8", errors="replace") as self.file:
            self.file.write(json.dumps([], sort_keys=False, indent=4))

    def get_entries(self):
        try:
            with open(self.file_path, 'r') as self.file:
                self.data = json.load(self.file)
                print("DATA:", self.data)
        except FileNotFoundError:
            print("NOT FOUND?")
        print(self.data)
        return self.data


class BaseDirectoryIO:

    def __init__(self, dir_path=''):
        self.dir_path = dir_path

    def __call__(self):
        return self.dir_path


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates job temp folder and stores path in _MEIPASS
        import sys
        base_path = sys._MEIPASS
        base_path = os.path.abspath(".")
        print("DIRFILES:", os.listdir(os.curdir))
    except AttributeError:
        print("DIRFILES:",os.listdir(os.curdir))
        base_path = os.path.abspath(".") if 'python38.dll' in os.listdir(os.curdir) else os.path.abspath("..")

    print(os.path.join(base_path, relative_path))
    return os.path.join(base_path, relative_path)
