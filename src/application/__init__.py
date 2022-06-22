"""
This module contains the basic functionalities for making multiple apps with the same general features. In your actual
apps, you should inherit this module and make your custom features to work with the available functionalities.

The following shows an example.
"""

from application.app import App
from application.gui import LabelCustom
from application.utils import ScreenUtil


class TestApp(App):

    def __init__(self):
        screen = ScreenUtil('Test',
                            placeholder=[LabelCustom('Hello World'),
                                         0.5,
                                         0.5])

        super().__init__(title='Test Application',
                         logo='../resources/images/logo.png',
                         dimensions=[1000, 1000],
                         lock=False,
                         screens=[screen()])


if __name__ == '__main__':
    TestApp()
