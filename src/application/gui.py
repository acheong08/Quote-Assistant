import time
from tkinter import *
from tkinter import filedialog, messagebox
from typing import Any, List, Dict, Tuple

# from src.application.defaults import DEFAULT_DPI

MASTER_THEME = {'fg': 'white',
                'fgh': '#ff6900',
                'bg': 'black',
                'font': ('Bahnschrift', 24)}


class WidgetCustom:
    """Custom widget base class to set default functions and values for all
    relevant widgets in the application."""

    default_font = MASTER_THEME['font']
    btn_pressed = False

    def __init__(self, widget_type, *args, config_custom=None, text_var=StringVar, int_var=None, **kwargs):
        self.d_font = WidgetCustom.default_font
        self.displayable = True
        self.widget = None
        self.widget_type = widget_type
        self.text = text_var
        self.var = int_var
        self.args = args
        self.kwargs = kwargs
        self.x_val = 0
        self.y_val = 0
        self.config = config_custom
        self.toggle_state = 1
        print("CONFIG: ", self.config, config_custom)

    def place_custom(self, x_val: float = 0., y_val: float = 0.):

        """Method to make placing widgets on the screen easier.

        Parameters:
            x_val: rel-x position on window
            y_val: rel-y position on window"""

        # Updates x and y values
        self.x_val = x_val
        self.y_val = y_val
        try:
            self.widget.place(relx=x_val, rely=y_val, anchor=CENTER)
        except AttributeError:
            self.place(x_val, y_val, CENTER)
        finally:
            pass

    def get_value(self, data_type: type = str):

        """Method to return the widget's text value."""

        try:
            print(self.widget.get(), data_type)
            return 0. if self.widget.get() == '' and data_type is float else data_type(self.widget.get())
        except ValueError:
            return self.widget.get()
        except AttributeError:
            if type(self.widget) is Checkbutton:
                return self.var.get()
            return self.text.get()
        finally:
            print("There is no value to be found.")

    def set_value(self, value):
        """Method to set job label's text value."""
        try:
            self.text.set(value)
            # print('---s')
        except AttributeError:
            print('---f')
            pass

    def toggle_widget(self, desired_state=0):

        """Method to make toggling the widget's appearance easier."""

        if self.displayable and desired_state == 0:
            print(self.__str__(), 'Toggled off')
            self.widget.place_forget()
            # if type(self) == FormInput:
            #     self.border.place_forget()
        elif not self.displayable and desired_state == 1:
            print(self.__str__(), 'Toggled on')
            self.place_custom(self.x_val, self.y_val)
        else:
            print('Nothing happened to', self.__str__())
            return
        self.displayable = not self.displayable

    def place(self, *args):
        print(self, "'s ", *args, " unused.", sep='')
        return None

    def initialize(self, widget_type, window, args, kwargs):
        """
        This method is what truly contructs the widget objects through tkinter, and places them on a screen. Typical
        use case for this is when a screen is displayed in screen manager for the first time.

        @param widget_type: what type of widget is going to be initialized (Tkinter object)
        @param window: the tkinter root widget
        @param args: any arguments to be passed into the widget constructor
        @param kwargs: any keyword arguments to be passed into the widget constructor
        """
        print("-----", widget_type, args, kwargs)

        # I forgot why I needed to put this in tbh
        if self.text is not None and widget_type is not Radiobutton:
            print('ADDING TEXT TO', widget_type, 'OBJECT')
            try:
                val = kwargs['text']
                try:
                    kwargs.pop('textvariable')
                except KeyError:
                    pass
            except KeyError:
                print("KEY ERROR")
                val = ''
            # self.widget.configure(textvariable=self.text)
            self.text = StringVar(window, value=val)

        # Where every single widget is constructed
        self.widget = widget_type(window, *args, **kwargs, textvariable=self.text)

        # Some widgets need additional configuration after they are created, so this can be used for those cases
        print("CONFIG TEST:", self.config)
        if self.config is not None:
            print("RUNNING CONFIG ON", self)
            self.widget.config(**self.config)

        # Checkbutton objects should use an integer variable instead of a text variable
        if type(self.widget) == Checkbutton:
            self.var = IntVar()
            self.widget.configure(variable=self.var)
            # self.widget.config(width=15)

        # Optional additional configurations
        self.initialize_custom()

    def initialize_custom(self):
        """
        Empty method that can be overriden by subclasses to add additional functionality during initialization phase.
        """
        pass


class LabelCustom(WidgetCustom):
    """Form label subclass of form widget.

    Creates job default Label widget based on settings for the form."""

    def __init__(self,
                 content='',
                 font_style=WidgetCustom.default_font,
                 font_size=WidgetCustom.default_font[1],
                 w=25,
                 height=1,
                 border=0,
                 fg_color=MASTER_THEME['fg'],
                 bg_color=MASTER_THEME['bg']):
        self.text = StringVar
        # self.widget = Label(window,
        #                     text=content,
        #                     font=d_font_style,
        #                     width=d_width,
        #                     height=d_height,
        #                     bd=d_border,
        #                     fg=d_fg_color,
        #                     bg=d_bg_color,
        #                     textvariable=self.text)
        kwargs = dict(text=content,
                      font=(font_style[0], font_size),
                      width=w,
                      height=height,
                      borderwidth=border,
                      fg=fg_color,
                      bg=bg_color,
                      # relief='sunken',
                      textvariable=self.text)
        # self.text.set(content)
        super().__init__(Label, **kwargs)


class InputCustom(WidgetCustom):
    """Form input subclass of form widget.

    Creates job default Entry widget based on settings for the form."""

    def __init__(self,
                 d_font_style=WidgetCustom.default_font,
                 w=14,
                 d_fg_color=MASTER_THEME['fg'],
                 d_bg_color=MASTER_THEME['bg']):
        # self.border = Frame(window,
        #                     background="white",
        #                     width=d_width * DEFAULT_DPI / 6.85,
        #                     height=2.5 * DEFAULT_DPI / 6.85, )
        kwargs = dict(font=d_font_style,
                      width=w,
                      fg=d_fg_color,
                      bg=d_bg_color,
                      bd=6)

        super().__init__(Entry, **kwargs)


class OptionMenuCustom(WidgetCustom):
    """Form option menu subclass of form widget.

    Creates job default OptionMenu widget based on settings for the form."""

    def __init__(self,
                 *values,
                 default_text='Select an Option',
                 font_size=18,
                 w=17,
                 theme=None):
        if theme is None:
            theme = MASTER_THEME
        self.text = None
        self.default_text = default_text
        configuration = dict(width=w,
                             bg=theme['bg'],
                             fg=theme['fg'],
                             font=(theme['font'][0], font_size))
        # configuration = {'width': d_width,
        #                  'bg': theme['bg'],
        #                  'fg': theme['fg'],
        #                  'font': theme['font']}
        print("---OPTION MENU:", configuration)
        super().__init__(OptionMenu, *values, config_custom=configuration, text=self.text)

    def initialize(self, widget_type, window, args, kwargs):
        self.text = StringVar()
        self.widget = OptionMenu(window, self.text, args[0], *(args[1:]))
        self.widget.configure(textvariable=self.text)
        self.widget.config(**self.config)
        self.text.set(self.default_text)

    def get_value(self, data_type: type = str):
        data = data_type(self.text.get())
        return '' if data == self.default_text else data


# noinspection PyTypeChecker
class ButtonCustom(WidgetCustom):
    """Form reset button subclass of form widget.

    Creates job Button widget based on settings for the form. Configured to run
    job command to reset the application when clicked."""

    def __init__(self, cmd, content='', w=5, h=1, f="white", b="black",
                 font_style=WidgetCustom.default_font,
                 font_size=WidgetCustom.default_font[1]):
        kwargs = dict(text=content,
                      width=w,
                      height=h,
                      font=(font_style[0], font_size),
                      fg=f,
                      bg=b,
                      # bd=0,
                      highlightthickness=1,
                      command=cmd)
        configuration=dict(highlightbackground='red', highlightcolor='red')
        super().__init__(Button, **kwargs, text_var=None, config_custom=configuration)

class CheckbuttonCustom(WidgetCustom):

    def __init__(self, content='', theme=None):
        if theme is None:
            theme = MASTER_THEME
        kwargs = dict(text=content,
                      font=super().default_font,
                      fg=theme['fgh'],
                      bg=theme['bg'],
                      bd=0,
                      onvalue=1,
                      offvalue=0)
        super().__init__(Checkbutton, **kwargs)

    def get_value(self, data_type: type = str):
        return True if self.var.get() == 1 else False

class RadioButtonCustom(WidgetCustom):

    def __init__(self, var, content='', state='0'):
        kwargs = dict(text=content,
                      font=super().default_font,
                      fg="#ff6900",
                      bg="black",
                      bd=1,
                      height=1,
                      # onvalue=1,
                      # offvalue=0,
                      value=state)
        super().__init__(Radiobutton, text_var=var, **kwargs)



class RadioButtonsCustom(WidgetCustom):
    # widgets: List[List[RadioButtonCustom, float, float]]
    widgets: List[RadioButtonCustom]
    variable: StringVar

    def __init__(self, *args, **kwargs):
        self.widgets = []
        self.variable = None
        self.previous_state = ''
        for val, arg in enumerate(args):
            self.widgets.append(RadioButtonCustom(self.variable, arg, str(val)))

        super().__init__(Radiobutton, *args, **kwargs)

    def get_selection(self):
        return self.variable.get()

    def place_custom(self, x_val: float = 0., y_val: float = 0.):
        for offset, widget in enumerate(self.widgets):
            widget.place_custom(x_val, y_val + 0.075 * offset)
            # widget.widget.place(relx=x_val, rely=y_val + 0.05 * offset, anchor=CENTER)
            print(widget)
            print("POSITION:", x_val, y_val + 0.05 * offset)

    def initialize(self, widget_type, window, args, kwargs):
        self.variable = StringVar()
        for widget in self.widgets:
            widget.kwargs['variable'] = self.variable
            widget.initialize(widget_type, window, widget.args, widget.kwargs)
            print(widget)
            widget.widget.config(width=20)
        # self.variable.set('0')

    def toggle_widget(self, desired_state=0):
        for widget in self.widgets:
            widget.toggle_widget(desired_state)


# noinspection PyTypeChecker
class FileButtonCustom(WidgetCustom):
    """Form file button subclass of form widget.

    Creates job Button widget based on settings for the form. Configured to open
    job file dialog input system when clicked."""
    file_type: str

    def __init__(self, validated_cmd, invalidated_cmd=None, data_type='txt'):
        kwargs = dict(text="Browse File System",
                      font=super().default_font,
                      fg=MASTER_THEME['fg'],
                      bg=MASTER_THEME['bg'],
                      borderwidth=5,
                      command=self._browse_files)
        self.validated_cmd = validated_cmd
        self.invalidated_cmd = invalidated_cmd
        self.file_type = data_type
        self.file_name = ''
        self.inputted = False
        super().__init__(Button, **kwargs, text_var=None)

    def _browse_files(self):

        """Internal method to manage the filedialog window and resultantly
        attain the file path."""

        temp_name = filedialog.askopenfilename(title="Select job File",
                                               filetypes=(("File", str("." + self.file_type)),
                                                          ("all files", "*.*")))
        if self.file_name != '' and temp_name == '':
            return

        self.file_name = temp_name
        print(self.file_name)
        if self.file_name[-len(self.file_type):] == self.file_type:
            self.widget.configure(text='File inputted.')
            self.inputted = True
            self.validated_cmd(self.file_name)
        elif self.invalidated_cmd is not None:
            self.invalidated_cmd()

    def get_file_lines(self):

        """Method to retrieve file lines separated as list items."""

        if self.file_name == '':
            return ['']
        file = open(self.file_name, "r", encoding="utf-8", errors="replace")
        lines = file.read().splitlines()
        file.close()
        return lines

    def get_file_path(self):
        return self.file_name

    def is_file_inputted(self) -> bool:
        return True if self.inputted else False


class ErrorManager:
    """Class that manages the error popup in tkinter."""

    def __init__(self):
        self.error_history = []

    def display(self, message='Something went Wrong.', header='Error'):
        """
        Method that displays the pop up with a custom message.

        @param header: the text to display as the popup header
        @param message: the text to display as the error message
        """
        self.error_history.append(message)
        messagebox.showerror(header, message)


class ScreenCustom:
    """Class that manages a tkinter screen and its widgets."""

    widgets: Dict[str, WidgetCustom]

    def __init__(self, screen_manager, name, geometry, **kwargs):
        assert isinstance(screen_manager, ScreenManager)
        self._screen_manager = screen_manager
        self.widgets = {}
        self._name = name
        self._geometry = geometry
        self.kwargs = kwargs
        self.initialize_widgets()

    def get_name(self):
        return self._name

    def get_geometry(self):
        return self._geometry

    def initialize_widgets(self):
        """
        Method that initializes a screen's widgets when prompted.
        """

        # Widgets are reset in the case of a screen re-initialize
        self.widgets = {}
        # kwargs hold the original values and positions of all widgets in the screen, so iteration is used to loop
        # through each indivudal widget (in index 0) as well as its corresponding position (index 1-2)
        for kwarg in self.kwargs:
            # Value is extract from the dictionary
            kwval = self.kwargs[kwarg]
            # Widget is added to the array
            self.widgets[kwarg] = kwval[0]
            # Widget is then initialized
            self.widgets[kwarg].initialize(self.widgets[kwarg].widget_type,
                                           self._screen_manager.window,
                                           self.widgets[kwarg].args,
                                           self.widgets[kwarg].kwargs)
            print(kwval)
            # Widget is then placed on the screen
            self.widgets[kwarg].place_custom(kwval[1], kwval[2])
            self.widgets[kwarg].displayable = True
            # Widget is then immediately removed from the screen because it may not be required.
            self.widgets[kwarg].toggle_widget(0)
            # Toggle state is set to a default of 1 (on) unless prompted otherwise
            self.widgets[kwarg].toggle_state = 1 if len(kwval) < 4 else kwval[3]
            print("KWA:", kwarg, "| KWV:", kwval, "| TOGGLE:", self.widgets[kwarg].toggle_state)

    def set_screen(self):
        """
        Method that sets the screen object in question as the current (display) screen.
        """

        # Transitioning variable set to disrupt other threads, giving time to do so
        self._screen_manager.transitioning = True
        time.sleep(0.05)
        # Conditional ensuring there IS a screen that needs to be taken down (exception being initial boot)
        if self._screen_manager.current_screen is not Ellipsis:
            print(self._screen_manager.current_screen)
            # Iterating widgets in the previous screen to be removed from the window
            for widget in self._screen_manager.current_screen.widgets:
                self._screen_manager.current_screen.widgets[widget].toggle_widget(0)
        time.sleep(0.05)
        # The window geometry is modified to whatever is specified by this screen
        self._screen_manager.modify_geometry(*self._geometry) if self._geometry is not None else None
        # Iterating widgets in this screen to be displayed to the window
        for widget in self.widgets:
            self.widgets[widget].toggle_widget(self.widgets[widget].toggle_state)
        # Previous screen set in case it is required for later implementation
        self._screen_manager.previous_screen = self._screen_manager.current_screen
        # Current screen is set as itself in the screen manager so it is easily accessible
        self._screen_manager.current_screen = self
        # Transitioning set to false to end disruptions
        self._screen_manager.transitioning = False

    def reset_screen(self):
        """
        Method that resets the screen (returns all widgets to original states).
        """

        self._screen_manager.transitioning = True
        self.initialize_widgets()
        self.set_screen()

    # def initialize_screen(self, window):
    #     for n, widget in enumerate(self.widgets):
    #         self.widgets[n].initialize(widget, window, )
    #         self.widgets[n].toggle_widget()


class ScreenManager:
    """Class that handles the management of one or more screens within thes application."""

    previous_screen: ScreenCustom
    current_screen: ScreenCustom

    def __init__(self, window, locked=False):
        self.screens = {}
        self.locked = locked
        self.current_screen = ...
        self.previous_screen = ...
        self.transitioning = False
        self.window = window

    def __call__(self, *args, **kwargs) -> ScreenCustom:
        """
        This method calls every time the object is called after initialization. It essentially returns a screen
        object, either the name entered as an argument or the current screen if no argument exists.

        @return: screen object
        """
        return self.current_screen if len(args) == 0 else self.get_screen(args[0])

    def get_screen(self, name: str = '', index: int = 0):
        """
        Method that retrieves a screen object manually with multiple options of retrieval

        @param name: name of the screen, if applicable
        @param index: index of the screen in the screens dictionary, if applicable
        @return: screen object
        """

        screen: ScreenCustom = self.screens[list(self.screens)[index]] if name == '' else self.screens[name]
        return screen

    def add_screen(self, name, geometry: Tuple[int, int], kwargs) -> None:
        """
        Method that adds a screen to the screen manager.

        @param name: name of the screen
        @param geometry: box_dimensions of the screen in (x, y) format
        @param kwargs: should be used for widgets and their locations
        """
        print('SCREEN KWARGS: ', kwargs)
        self.screens[name] = ScreenCustom(self, name, geometry, **kwargs)

    def modify_geometry(self, x, y):
        """
        Changes the size of the window which is displaying the screen.

        @param x: specified length of the window
        @param y: specified height of the window
        """
        if self.locked:
            self.window.minsize(width=x, height=y)
            self.window.maxsize(width=x, height=y)
        self.window.geometry(str(x)+'x'+str(y))

