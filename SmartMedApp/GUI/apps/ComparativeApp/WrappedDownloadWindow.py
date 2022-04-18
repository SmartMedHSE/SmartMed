import pickle
import pandas as pd

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QToolTip, QPushButton, QApplication, QMessageBox)

from .DownloadWindow import DownloadWindow
from ..Notification import NotificationWindow
from ..utils import *

from backend.modules.dataprep import PandasPreprocessor


class WrappedDownloadWindow(DownloadWindow, QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.__build_buttons()
        self.setWindowTitle('Загрузка данных')
        self.settings = {'MODULE': 'COMPARATIVE', 'MODULE_SETTINGS': {'path': '', 'columns': '',
                                                                      'preprocessing': '', 'type': '', 'methods': ''}}
        self.columns = ''

    def __build_buttons(self):
        self.pushButtonBack.clicked.connect(self.back)
        self.pushButtonNext.clicked.connect(self.next)
        self.pushButton.clicked.connect(self.path_to_file)

    def back(self):
        remove_if_exists()
        self.hide()
        self.parent.show()

    def next(self):
        while self.settings['MODULE_SETTINGS']['path'] == '':
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Ошибка")
            msg.setInformativeText('Выберите файл')
            msg.setWindowTitle("Ошибка")
            msg.exec_()
            return
        while len(read_file(self.settings['MODULE_SETTINGS']['path'])) < 1:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Ошибка")
            msg.setInformativeText('Слишком мало данных')
            msg.setWindowTitle("Ошибка")
            msg.exec_()
            return
        while len(get_class_columns(self.settings['MODULE_SETTINGS']['path'], 10)) == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Ошибка")
            msg.setInformativeText('Отсутсвуют категориальные коллонки')
            msg.setWindowTitle("Ошибка")
            msg.exec_()
            return
        self.hide()
        self.child.show()

    def path_to_file(self):
        path = QtWidgets.QFileDialog.getOpenFileName()[0]
        if path != '':
            self.settings['MODULE_SETTINGS']['path'] = path
            self.settings['MODULE_SETTINGS']['columns'] = read_file(path).columns
        with open('settings.py', 'wb') as f:
            pickle.dump(self.settings, f)

