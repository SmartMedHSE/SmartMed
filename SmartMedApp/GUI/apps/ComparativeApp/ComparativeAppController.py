from .WrappedDownloadWindow import WrappedDownloadWindow
from .WrappedPreprocessingWindow import WrappedPreprocessingWindow
from .WrappedVariablesTypeWindow import WrappedVariablesTypeWindow
from .WrappedContinuousMethods import WrappedContinuousMethods
from .WrappedCategoricalMethods import WrappedCategoricalMethods

from logs.logger import debug


class ComparativeApp():

    @debug
    def __init__(self, menu_window):
        self.settings = {}
        self.menu_window = menu_window
        self.down_window = WrappedDownloadWindow()
        self.prep_window = WrappedPreprocessingWindow()
        self.var_type_window = WrappedVariablesTypeWindow()
        self.cont_window = WrappedContinuousMethods()
        self.cat_window = WrappedCategoricalMethods()

        self.__build_connections(
            [self.menu_window, self.down_window, self.prep_window, self.var_type_window])

    @debug
    def __build_connections(self, ordered_windows):

        ordered_windows[0].child = ordered_windows[1]
        ordered_windows[0].parent = ordered_windows[-1]

        ordered_windows[-1].child = ordered_windows[0]
        ordered_windows[-1].parent = ordered_windows[-2]

        for i in range(1, len(ordered_windows) - 1):
            ordered_windows[i].child = ordered_windows[i + 1]
            ordered_windows[i].parent = ordered_windows[i - 1]

        self.var_type_window.child_cont = self.cont_window
        self.cont_window.parent = self.var_type_window
        self.cont_window.child = self.menu_window

        self.var_type_window.child_cat = self.cat_window
        self.cat_window.parent = self.var_type_window
        self.cat_window.child = self.menu_window

    @debug
    def start(self):
        self.down_window.show()
