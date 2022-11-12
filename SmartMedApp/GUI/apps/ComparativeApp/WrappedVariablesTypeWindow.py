import pickle

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QWidget, QToolTip, QPushButton, QApplication, QMessageBox, QTableWidget)

from .VariablesTypeWindow import VariablesTypeWindow


class WrappedVariablesTypeWindow(VariablesTypeWindow, QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Выбор типа переменных')
        self.__build_buttons()
        self.radioButton_continuous.setChecked(True)

    def __build_buttons(self):
        self.pushButtonNext.clicked.connect(self.next)
        self.pushButtonBack.clicked.connect(self.back)

    def back(self):
        self.hide()
        self.parent.show()

    def next(self):
        self.hide()
        with open('settings.py', 'rb') as f:
            data = pickle.load(f)

        if self.radioButton_continuous.isChecked():
            data['MODULE_SETTINGS'].update({'type': 'continuous'})
            self.child_cont.show()
        else:
            data['MODULE_SETTINGS'].update({'type': 'categorical'})
            self.child_cat.show()

        with open('settings.py', 'wb') as f:
            pickle.dump(data, f)
