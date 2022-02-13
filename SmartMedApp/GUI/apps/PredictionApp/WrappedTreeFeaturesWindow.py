import pickle
import threading

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QWidget, QToolTip, QPushButton, QApplication, QMessageBox, )

from .TreeFeaturesWindow import TreeFeaturesWindow


class WrappedTreeFeaturesWindow(TreeFeaturesWindow, QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.__build_buttons()
        self.settings = {'sort': True}
        self.checkBox.setChecked(True)

    def __build_buttons(self):
        self.pushButtonNext.clicked.connect(self.next)
        self.pushButtonBack.clicked.connect(self.back)
        self.checkBox.clicked.connect(self.sort)
        self.setWindowTitle(' ')

    def back(self):
        self.hide()
        self.parent.show()

    def sort(self):
        if self.checkBox.isChecked():
            self.checkBox.setChecked(True)
            self.settings['sort'] = True
        else:
            self.checkBox.setChecked(False)
            self.settings['sort'] = False

    def next(self):
        depth = self.lineEdit.text()
        min_sample_number = self.lineEdit_2.text()
        features_count = self.lineEdit_3.text()
        while (depth.isdigit() is False and min_sample_number.isdigit() is False\
                and features_count.isdigit() is False) or (bool(depth.strip()) and bool(min_sample_number.strip())
                                                           and bool(features_count.strip())):
            if bool(depth.strip()) is False and bool(min_sample_number.strip()) is False and\
                    bool(features_count.strip()) is False:
                break
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Ошибка")
                msg.setInformativeText('Неверный формат параметров')
                msg.setWindowTitle("Ошибка")
                msg.exec_()
                return

        with open('settings.py', 'rb') as f:
            data = pickle.load(f)
            col = data['MODULE_SETTINGS']['columns'].to_list()
            if features_count.strip() != '':
                if int(features_count) > len(col) - 1:
                    features_count = int(len(col) - 1)
            data['MODULE_SETTINGS'].update({'tree_depth': depth.strip(),
                                            'samples': min_sample_number.strip(),
                                            'features_count': features_count.strip()})
            data['MODULE_SETTINGS'].update(self.settings)
        with open('settings.py', 'wb') as f:
            pickle.dump(data, f)

        self.hide()
        self.child.show()
