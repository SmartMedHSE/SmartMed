import pickle

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QWidget, QToolTip,
                             QPushButton, QApplication, QMessageBox)
import pandas as pd
import pickle

from .TaskWindow import TaskWindow


class WrappedTaskWindow(TaskWindow, QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Сравнение')
        self.__build_buttons()

    def __build_buttons(self):
        self.pushButtonBack.clicked.connect(self.back)
        self.pushButtonNext.clicked.connect(self.next)

    def listview_clicked(self):
        item = self.list1.currentItem()

        # self.label.setText(str(item.text()))

    def back(self):
        self.hide()
        self.parent.show()

    def next(self):
        with open('settings.py', 'rb') as f:
            data = pickle.load(f)
            data['MODULE_SETTINGS']['metrics'].update(self.settings)

        with open('settings.py', 'wb') as f:
            pickle.dump(data, f)

        self.hide()
        self.child.show()


