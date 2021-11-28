# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TreeVisualWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class TreeVisualWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 480)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(70, 30, 521, 81))
        self.label.setObjectName("label")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(110, 140, 600, 200))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.checkBoxTree = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBoxTree.setObjectName("checkBoxTree")
        self.verticalLayout.addWidget(self.checkBoxTree)
        self.checkBoxTablr = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBoxTablr.setObjectName("checkBoxTablr")
        self.verticalLayout.addWidget(self.checkBoxTablr)
        self.checkBoxValue = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBoxValue.setObjectName("checkBoxValue")
        self.verticalLayout.addWidget(self.checkBoxValue)
        self.checkBoxDistributions = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBoxDistributions.setObjectName("checkBoxDistributions")
        self.verticalLayout.addWidget(self.checkBoxDistributions)
        self.checkBoxPrediction = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBoxPrediction.setObjectName("checkBoxPrediction")
        self.verticalLayout.addWidget(self.checkBoxPrediction)
        self.pushButtonDone = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonDone.setGeometry(QtCore.QRect(460, 420, 113, 32))
        self.pushButtonDone.setObjectName("pushButtonDone")
        self.pushButtonBack = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonBack.setGeometry(QtCore.QRect(330, 420, 113, 32))
        self.pushButtonBack.setObjectName("pushButtonBack")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:18pt;\">Выберите таблицы и графики </span></p><p><span style=\" font-size:18pt;\"></span></p></body></html>"))
        self.checkBoxTree.setText(_translate("MainWindow", "  Графическое преставление дерева"))
        self.checkBoxTablr.setText(_translate("MainWindow", "  Классификационная таблица, в которой наблюдаемые показатели\n  "
"противопоставляются предсказанным "))
        self.checkBoxValue.setText(_translate("MainWindow", "  Показатели построенного дерева"))
        self.checkBoxDistributions.setText(_translate("MainWindow", "  График распределения классов"))
        self.checkBoxPrediction.setText(_translate("MainWindow", "  Блок по предсказанию"))
        self.pushButtonDone.setText(_translate("MainWindow", "Завершить"))
        self.pushButtonBack.setText(_translate("MainWindow", "Назад"))
