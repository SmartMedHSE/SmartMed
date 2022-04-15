import pickle
import numpy as np
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
        num = list(np.array(np.arange(0, 100)).astype(str))
        num[0] = 'По умолчанию'
        num_samples = list(np.array(np.arange(1, 100)).astype(str))
        num_samples[0] = 'По умолчанию'
        self.comboBoxDepth.addItems(num)
        self.comboBoxMinSample.addItems(num_samples)
        self.comboBoxFeatureCount.addItems(num)

    def __build_buttons(self):
        self.pushButtonNext.clicked.connect(self.next)
        self.pushButtonBack.clicked.connect(self.back)
        self.checkBox.clicked.connect(self.sort)
        self.setWindowTitle('Выбор параметров дерева')

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
        depth = self.comboBoxDepth.currentText()
        min_sample_number = self.comboBoxMinSample.currentText()
        features_count = self.comboBoxFeatureCount.currentText()

        if depth == 'По умолчанию':
            depth = None
        else:
            depth = int(depth)
        if min_sample_number == 'По умолчанию':
            min_sample_number = 2
        else:
            min_sample_number = int(min_sample_number)
        if features_count == 'По умолчанию':
            features_count = None
        else:
            features_count = int(features_count)

        with open('settings.py', 'rb') as f:
            data = pickle.load(f)
            col = data['MODULE_SETTINGS']['columns'].to_list()
            if features_count is not None:
                if int(features_count) > len(col) - 1:
                    features_count = int(len(col) - 1)
            data['MODULE_SETTINGS'].update({'tree_depth': depth,
                                            'samples': min_sample_number,
                                            'features_count': features_count})
            data['MODULE_SETTINGS'].update(self.settings)
        with open('settings.py', 'wb') as f:
            pickle.dump(data, f)

        self.hide()
        self.child.show()
