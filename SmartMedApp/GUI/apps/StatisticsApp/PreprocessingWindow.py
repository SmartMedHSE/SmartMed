# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DownloadWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.



from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QListWidget
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import pandas


class ListWidget(QListWidget):
    def clicked(self, item):
        QMessageBox.information(self, "ListWidget", "ListWidget: " + item.text())

class PreprocessingWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(850, 500)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(50, 120, 461, 81))
        self.label_2.setObjectName("label_2")
        self.pushButtonBack = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonBack.setGeometry(QtCore.QRect(50, 440, 113, 32))
        self.pushButtonBack.setObjectName("pushButtonBack")
        self.pushButtonNext = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonNext.setGeometry(QtCore.QRect(640, 440, 113, 32))
        self.pushButtonNext.setObjectName("pushButtonNext")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 30, 251, 51))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(50, 250, 183, 32))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)

        self.pushButtonBuild = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonBuild.setGeometry(QtCore.QRect(335, 440, 130, 32))
        self.pushButtonBuild.setToolTipDuration(10)
        self.pushButtonBuild.setObjectName("pushButtonBuild")

        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(400, 50, 400, 300))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.list1 = QListWidget()

        self.list1.clicked.connect(self.list1view_clicked)
        # self.list.setGeometry(QtCore.QRect(100, 100, 100, 100))
        self.horizontalLayout.addWidget(self.list1)

        self.list2 = QListWidget()

        self.list2.clicked.connect(self.list2view_clicked)
        # self.list.setGeometry(QtCore.QRect(100, 100, 100, 100))
        self.horizontalLayout.addWidget(self.list2)

        self.list3 = QListWidget()
        # self.fillList()
        self.list3.clicked.connect(self.list3view_clicked)
        # self.list.setGeometry(QtCore.QRect(100, 100, 100, 100))
        self.horizontalLayout.addWidget(self.list3)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p>Для того, чтобы выполнить загрузку данных, кликните </p><p>на кнопку ниже. В открывшемся окне выберите файл</p><p>в формате &quot;xlsx&quot;, &quot;csv&quot;, &quot;tsv&quot;.</p><p><br/></p></body></html>"))
        self.pushButtonBack.setText(_translate("MainWindow", "Назад"))
        self.pushButtonNext.setText(_translate("MainWindow", "Вперед"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:13pt;\">Загрузите данные</span></p></body></html>"))
        self.pushButton.setText(_translate("MainWindow", "Загрузить"))
        self.pushButtonBuild.setText(_translate("MainWindow", "Построить график"))
