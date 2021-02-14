# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'VisualizationWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 480)
        MainWindow.setToolTipDuration(4)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButtonDone = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonDone.setGeometry(QtCore.QRect(470, 430, 113, 32))
        self.pushButtonDone.setObjectName("pushButtonDone")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(340, 430, 113, 32))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(70, 30, 301, 31))
        self.label.setObjectName("label")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(70, 70, 356, 321))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.checkBoxCorr = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBoxCorr.setObjectName("checkBoxCorr")
        self.verticalLayout.addWidget(self.checkBoxCorr)
        self.checkBoxScatter = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBoxScatter.setAcceptDrops(False)
        self.checkBoxScatter.setIconSize(QtCore.QSize(20, 20))
        self.checkBoxScatter.setObjectName("checkBoxScatter")
        self.verticalLayout.addWidget(self.checkBoxScatter)
        self.checkBoxHist = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBoxHist.setObjectName("checkBoxHist")
        self.verticalLayout.addWidget(self.checkBoxHist)
        self.checkBoxHeatmap = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBoxHeatmap.setObjectName("checkBoxHeatmap")
        self.verticalLayout.addWidget(self.checkBoxHeatmap)
        self.checkBoxDot = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBoxDot.setToolTipDuration(0)
        self.checkBoxDot.setObjectName("checkBoxDot")
        self.verticalLayout.addWidget(self.checkBoxDot)
        self.checkBoxLinear = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBoxLinear.setObjectName("checkBoxLinear")
        self.verticalLayout.addWidget(self.checkBoxLinear)
        self.checkBoxBox = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBoxBox.setObjectName("checkBoxBox")
        self.verticalLayout.addWidget(self.checkBoxBox)
        self.checkBoxBar = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBoxBar.setObjectName("checkBoxBar")
        self.verticalLayout.addWidget(self.checkBoxBar)
        self.checkBoxLog = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBoxLog.setObjectName("checkBoxLog")
        self.verticalLayout.addWidget(self.checkBoxLog)
        self.checkBoxPie = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBoxPie.setObjectName("checkBoxPie")
        self.verticalLayout.addWidget(self.checkBoxPie)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Визуализация"))
        self.pushButtonDone.setText(_translate("MainWindow", "Завершить"))
        self.pushButton.setText(_translate("MainWindow", "Назад"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:18pt;\">Выбор графиков для реализации</span></p></body></html>"))
        self.checkBoxCorr.setText(_translate("MainWindow", "матрица корреляций(в численном виде)"))
        self.checkBoxScatter.setText(_translate("MainWindow", "матрица корреляций(в виде диаграммы рассеяния)"))
        self.checkBoxHist.setText(_translate("MainWindow", "гистограмма"))
        self.checkBoxHeatmap.setText(_translate("MainWindow", "Тепловая карта"))
        self.checkBoxDot.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"center\">Это тул тип типочек молодой цыганенок я за тобой бегал месяц мразота</p></body></html>"))
        self.checkBoxDot.setText(_translate("MainWindow", "Точечная диаграмма "))
        self.checkBoxLinear.setText(_translate("MainWindow", "График линейной зависимости"))
        self.checkBoxBox.setText(_translate("MainWindow", "график ящик усы"))
        self.checkBoxBar.setText(_translate("MainWindow", "Столбцовая диаграмма"))
        self.checkBoxLog.setText(_translate("MainWindow", "График логарифмической зависимости"))
        self.checkBoxPie.setText(_translate("MainWindow", "Круговая диаграмма"))
