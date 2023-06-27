import pickle
import threading

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer, QEventLoop

from .CategoricalMethods import CategoricalMethods
from ..WaitingSpinnerWidget import QtWaitingSpinner
from ..utils import remove_if_exists

from backend import ModuleManipulator


class WrappedCategoricalMethods(CategoricalMethods, QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Категориальные переменные')
        self.settings = {
            'pearson': True,
            'se_sp': True,
            'odds_ratio': True,
            'risk_ratio': True
        }
        self.checkBoxPearson.setChecked(True)
        self.checkBoxSeSp.setChecked(True)
        self.checkBoxOddsRatio.setChecked(True)
        self.checkBoxRiskRatio.setChecked(True)
        self.__build_buttons()

    def __build_buttons(self):
        self.pushButtonBack.clicked.connect(self.back)
        self.pushButtonDone.clicked.connect(self.done)
        self.checkBoxPearson.clicked.connect(self.check_pearson)
        self.checkBoxSeSp.clicked.connect(self.check_se_sp)
        self.checkBoxOddsRatio.clicked.connect(self.check_odds_ratio)
        self.checkBoxRiskRatio.clicked.connect(self.check_risk_ratio)

    def back(self):
        self.hide()
        self.hide()
        self.parent.show()

    def done(self):
        with open('settings.py', 'rb') as f:
            data = pickle.load(f)
            data['MODULE_SETTINGS']['methods'] = self.settings

        with open('settings.py', 'wb') as f:
            pickle.dump(data, f)

        # with open('settings.py', 'rb') as f:
        #     settings = pickle.load(f)

        self.close()
        self.child.show()
        module_starter = ModuleManipulator(data)
        threading.Thread(target=module_starter.start, daemon=True).start()
        self.spinner = QtWaitingSpinner(self)
        self.layout().addWidget(self.spinner)
        remove_if_exists()
        self.spinner.start()
        # QTimer.singleShot(10000, self.spinner.stop)
        loop = QEventLoop()
        QTimer.singleShot(10000, loop.quit)
        loop.exec_()
        self.spinner.stop()
        print(data)

    def check_pearson(self):

        if self.checkBoxPearson.isChecked():
            self.checkBoxPearson.setChecked(True)
            self.settings['pearson'] = True
        else:
            self.checkBoxPearson.setChecked(False)
            self.settings['pearson'] = False

    def check_se_sp(self):
        if self.checkBoxSeSp.isChecked():
            self.checkBoxSeSp.setChecked(True)
            self.settings['se_sp'] = True
        else:
            self.checkBoxSeSp.setChecked(False)
            self.settings['se_sp'] = False

    def check_odds_ratio(self):
        if self.checkBoxOddsRatio.isChecked():
            self.checkBoxOddsRatio.setChecked(True)
            self.settings['odds_ratio'] = True
        else:
            self.checkBoxOddsRatio.setChecked(False)
            self.settings['odds_ratio'] = False

    def check_risk_ratio(self):
        if self.checkBoxRiskRatio.isChecked():
            self.checkBoxRiskRatio.setChecked(True)
            self.settings['risk_ratio'] = True
        else:
            self.checkBoxRiskRatio.setChecked(False)
            self.settings['risk_ratio'] = False
