import _tkinter
import os
import sys
import time

try:
    from application.constants import *
    from application.gui import *
    from application.utils import resource_path
except ImportError:
    # PyCharm is stupid, I'm stupid, we're all stupid.
    from src.application.constants import *
    from src.application.gui import *
    from src.application.utils import resource_path

from tkinter import *
from multitasking import task


class App:
    # app_fields: dict[str, Any]

    window: Tk = None
    current_inst: Tk = None

    app_fields_master = dict(title=DEFAULT_TITLE,
                             logo=DEFAULT_LOGO,
                             dpi=DEFAULT_DPI,
                             dimensions=DEFAULT_DIMENSIONS,
                             lock=DEFAULT_DIMENSIONS_LOCK,
                             background=DEFAULT_BACKGROUND,
                             screens=[DEFAULT_SCREEN])

    def __init__(self, *args, **kwargs):
        self.app_fields = App.app_fields_master
        imported_fields = kwargs

        for field in self.app_fields:
            try:
                self.app_fields[field] = imported_fields[field]
                imported_fields.pop(field, None)
            except KeyError:
                pass

        if len(imported_fields) > 0:
            print("[Error] Invalid fields:", ', '.join(list(imported_fields.keys())),
                  "\n--- Valid fields are the following:", ', '.join(list(App.app_fields_master.keys())),
                  file=sys.stderr)
            sys.exit(1)

        print(self.app_fields)

        self.window = Tk()
        self.locked = self.app_fields['lock']

        self.m_screen = ScreenManager(self.window, self.locked)
        self.m_error = ErrorManager()

        self.dim_x = self.app_fields['dimensions'][0]
        self.dim_y = self.app_fields['dimensions'][1]

        for screen in self.app_fields['screens']:
            print("SCREEN: ", screen)
            self.m_screen.add_screen(*screen)

        self.window.title(self.app_fields['title'])
        self.dpi = self.window.winfo_fpixels('1i')
        print("DPI:", self.dpi)
        self.dim_x = int(self.dim_x * self.dpi) // 96
        self.dim_y = int(self.dim_y * self.dpi) // 96
        self.window.geometry(str(self.dim_x) + 'x' + str(self.dim_y))
        self.window.config(background=self.app_fields['background'])
        if self.locked:
            self.window.minsize(width=self.dim_x, height=self.dim_y)
            self.window.maxsize(width=self.dim_x, height=self.dim_y)
        print(os.path.abspath(os.path.curdir))
        photo = PhotoImage(file=resource_path(self.app_fields['logo']))
        self.window.iconphoto(False, photo)

        App.current_inst = self
        self.m_screen.get_screen(index=0).set_screen()

        try:
            self.window.wm_attributes('-transparentcolor', DEFAULT_TRANS_COLOR)
        except _tkinter.TclError:
            print("Mac feature disables transparency.")

        self.running = True

        self._start_loop()

        self.window.mainloop()

        self.running = False

        os._exit(0)

    @task
    def _start_loop(self):
        self._loop()

    def _loop(self):
        while self.running:
            exit() if not self.running else None
            time.sleep(1. / DEFAULT_FPS)
            try:
                self.periodic() if not self.m_screen.transitioning else print("TRANSITIONING...")
            # except AttributeError:
            #     print("ATTRIBUTE ERROR IN PERIODIC.")
            #     exit()
            except KeyError:
                print("KEY ERROR IN PERIODIC.")
                exit()
            # self._loop()

    def periodic(self):
        pass




