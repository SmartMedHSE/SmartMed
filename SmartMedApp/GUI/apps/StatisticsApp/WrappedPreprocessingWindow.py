import pickle
import os

import pandas
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QWidget, QToolTip, QPushButton, QApplication, QMessageBox)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QMainWindow
from plotly.graph_objects import Figure, Scatter
import plotly
import numpy as np
from PyQt5.QtWidgets import QCheckBox
from .PreprocessingWindow import PreprocessingWindow
from ..utils import remove_if_exists
import plotly.graph_objects as go
from plotly.subplots import make_subplots



class WrappedPreprocessingWindow(PreprocessingWindow, QtWidgets.QMainWindow):

    def listview_clicked(self):
        item = self.list1.currentItem()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.list1Item = ''
        self.list2Item = ''
        self.list3Item = ''
        self.settings = {'MODULE_SETTINGS': {
            'metrics': {}, 'graphs': {}}, 'MODULE': 'STATS'}
        self.settings['MODULE_SETTINGS']['data'] = {'preprocessing': {
            'fillna': 'mean',
            'encoding': 'label_encoding',
            'scaling': False
        },
            'path': ''
        }
        self.__build_buttons()
        self.setWindowTitle('Загрузка данных')
        import matplotlib.pyplot as plt
        plt.plot([1, 2, 3, 4, 5], [10, 20, 30, 40, 50])
        '''
        self.comboBox1.addItems(["Средним/модой (численные/категориальные значения)",
                                 "Введенным значением (требуется ввод для каждого столбца отдельно)",
                                 "Удаление строк с пропущенными значениями",
                                 "Медианной/модой (численные/категориальные значения)"
                                 ])


'''

    def __build_buttons(self):
        self.pushButtonNext.clicked.connect(self.next)
        self.pushButtonBack.clicked.connect(self.back)
        self.pushButton.clicked.connect(self.path_to_file)
        self.pushButtonBuild.clicked.connect(self.build_graph)

    def back(self):
        remove_if_exists()
        self.hide()
        self.parent.show()

    def next(self):
        while self.settings['MODULE_SETTINGS']['data']['path'] == '':
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Ошибка")
            msg.setInformativeText('Выберите файл')
            msg.setWindowTitle("Ошибка")
            msg.exec_()
            return

            '''
        value_na = self.comboBox1.currentText()

        if value_na == 'средним/модой (аналогично)':
            self.settings['MODULE_SETTINGS']['data']['fillna'] = 'mean'
        elif value_na == 'заданным значием (требуется ввод для каждого столбца отдельно)':
            self.settings['MODULE_SETTINGS']['data']['fillna'] = 'exact_value'
        elif value_na == 'откидывание строк с пропущенными значениями':
            self.settings['MODULE_SETTINGS']['data']['fillna'] = 'dropna'
        else:
            self.settings['MODULE_SETTINGS']['data']['fillna'] = 'median'
        '''
        with open('settings.py', 'wb') as f:
            pickle.dump(self.settings, f)

        self.hide()
        self.child.show()

    def path_to_file(self):
        self.settings['MODULE_SETTINGS']['data'][
            'path'] = QtWidgets.QFileDialog.getOpenFileName()[0]
        self.data = pandas.read_excel(
            self.settings['MODULE_SETTINGS']['data']['path'])
        numerics = ['int16', 'int32', 'int64', 'float16', 'float32',
                    'float64']

        df = self.data.select_dtypes(include=numerics)
        for i in range(len(df.columns)):
            self.list1.insertItem(i, df.columns[i])
            self.list2.insertItem(i, df.columns[i])
            self.list3.insertItem(i, df.columns[i])

    def build_graph(self):
        print(self.list1Item)
        print(self.list2Item)
        print(self.list3Item)
        self.newindow = Window2(self.list1Item, self.list2Item,
                                self.list3Item, self.data)
        self.newindow.show()

    def list1view_clicked(self):
        self.list1Item = self.list1.currentItem().text()

    def list2view_clicked(self):
        self.list2Item = self.list2.currentItem().text()

    def list3view_clicked(self):
        self.list3Item = self.list3.currentItem().text()


class Window2(QtWidgets.QWidget):
    def __init__(self, item1, item2, item3, data):
        super(QtWidgets.QWidget, self).__init__()
        self.item1 = item1
        self.item2 = item2
        self.item3 = item3
        self.data = data
        self.initUI()

    def initUI(self):
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        # print(type(self.data[self.item1]))
        # self.data[self.item1].to_frame()
        # print(type(self.data[self.item1]))
        # print(self.data[self.item1])
        sorting_column = self.data[self.item1].name
        graph_2_col = self.data[self.item2].name
        graph_3_col = self.data[self.item3].name
        new_df_graph_1 = pandas.concat([self.data[self.item1], self.data[self.item2]],
                               axis=1)
        new_df_graph_2 = pandas.concat([self.data[self.item1], self.data[self.item3]],
                               axis=1)
        new_df_graph_1 = new_df_graph_1.sort_values(by=[sorting_column])
        new_df_graph_2 = new_df_graph_2.sort_values(by=[sorting_column])
        print(new_df_graph_1)
        print(new_df_graph_2)
        fig.add_trace(go.Scatter(
            x=new_df_graph_1[sorting_column].values,
            y=new_df_graph_1[graph_2_col].values,
            name=self.item2
        ))

        fig.add_trace(go.Scatter(
            x=new_df_graph_2[sorting_column].values,
            y=new_df_graph_2[graph_3_col].values,
            name=self.item3

        ))


        html = '<html><body>'
        html += plotly.offline.plot(fig, output_type='div',
                                    include_plotlyjs='cdn')
        html += '</body></html>'


        plot_widget = QWebEngineView()
        plot_widget.setHtml(html)

        self.verticalLayoutWidget = QtWidgets.QWidget(self)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 20, 800, 800))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)

        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.addWidget(plot_widget)


        self.show()