import pickle
import threading

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer, QEventLoop

from .ContinuousMethods import ContinuousMethods
from ..WaitingSpinnerWidget import QtWaitingSpinner
from ..utils import remove_if_exists

from SmartMedApp.backend import ModuleManipulator


class WrappedContinuousMethods(ContinuousMethods, QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Непрерывные переменные')
        self.settings = {
            'kolmagorova_smirnova': True,
            'student_independent': True,
            'student_dependent': True,
            'mann_whitney': True,
            'wilcoxon': True,
        }
        self.checkBoxKolmSmirn.setChecked(True)
        self.checkBoxStudentDepend.setChecked(True)
        self.checkBoxStudentIndepend.setChecked(True)
        self.checkBoxMannWhitney.setChecked(True)
        self.checkBoxWilcoxon.setChecked(True)
        self.__build_buttons()

    def __build_buttons(self):
        self.pushButtonBack.clicked.connect(self.back)
        self.pushButtonDone.clicked.connect(self.done)
        self.checkBoxKolmSmirn.clicked.connect(self.check_kolm_smirn)
        self.checkBoxStudentDepend.clicked.connect(self.check_student_dependent)
        self.checkBoxStudentIndepend.clicked.connect(self.check_student_independent)
        self.checkBoxMannWhitney.clicked.connect(self.check_mann_whitney)
        self.checkBoxWilcoxon.clicked.connect(self.check_wilcoxon)

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

    def check_kolm_smirn(self):

        if self.checkBoxKolmSmirn.isChecked():
            self.checkBoxKolmSmirn.setChecked(True)
            self.settings['kolmagorova_smirnova'] = True
        else:
            self.checkBoxKolmSmirn.setChecked(False)
            self.settings['kolmagorova_smirnova'] = False

    def check_student_dependent(self):

        if self.checkBoxStudentDepend.isChecked():
            self.checkBoxStudentDepend.setChecked(True)
            self.settings['student_dependent'] = True
        else:
            self.checkBoxStudentDepend.setChecked(False)
            self.settings['student_dependent'] = False

    def check_student_independent(self):

        if self.checkBoxStudentIndepend.isChecked():
            self.checkBoxStudentIndepend.setChecked(True)
            self.settings['student_independent'] = True
        else:
            self.checkBoxStudentIndepend.setChecked(False)
            self.settings['student_independent'] = False

    def check_mann_whitney(self):
        if self.checkBoxMannWhitney.isChecked():
            self.checkBoxMannWhitney.setChecked(True)
            self.settings['mann_whitney'] = True
        else:
            self.checkBoxMannWhitney.setChecked(False)
            self.settings['mann_whitney'] = False

    def check_wilcoxon(self):
        if self.checkBoxWilcoxon.isChecked():
            self.checkBoxWilcoxon.setChecked(True)
            self.settings['wilcoxon'] = True
        else:
            self.checkBoxWilcoxon.setChecked(False)
            self.settings['wilcoxon'] = False
