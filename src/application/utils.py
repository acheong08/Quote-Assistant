import os
from typing import TextIO


# from src.application.constants import *
# from src.application.gui import *


class ScreenUtil:

    def __init__(self, name: str, setup=None, **kwargs):
        self.name = name
        self.setup = setup
        self.widgets = kwargs
        self.screen = [name, self.widgets]
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
    except AttributeError:
        base_path = os.path.abspath("..")
    print(os.path.join(base_path, relative_path))
    return os.path.join(base_path, relative_path)
