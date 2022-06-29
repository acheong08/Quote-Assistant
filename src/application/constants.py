from typing import Tuple, List, Union, Dict, Any

# from src.application import LabelCustom
try:
    from application.gui import *
    from application.gui import LabelCustom
    from application.utils import resource_path
except ImportError:
    from src.application.gui import *
    from src.application.gui import LabelCustom
    from src.application.utils import resource_path

DEFAULT_LOGO: str = resource_path('resources/images/logo.png')
DEFAULT_DPI: float = 0.14
DEFAULT_DIMENSIONS: Tuple[int, int] = (500, 500)
DEFAULT_DIMENSIONS_LOCK: bool = True
DEFAULT_TITLE: str = 'Placeholder App'
DEFAULT_BACKGROUND: str = 'black'
DEFAULT_SCREEN = ['Test',
                  dict(placeholder=[
                      LabelCustom('Test'),
                      0.5,
                      0.25])]
DEFAULT_FPS = 60
DEFAULT_TRANS_COLOR: str = "#012345"
