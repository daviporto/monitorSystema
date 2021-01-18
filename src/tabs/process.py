import os

from PyQt5 import QtWidgets

from src.tables.Processes import Table

searchIcon = os.path.join('rsc', 'search.png')


class ProcessTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ProcessTab, self).__init__(parent=parent)
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.ln_processos = QtWidgets.QLineEdit(self)
        self.gridLayout.addWidget(self.ln_processos, 0, 0, 1, 1)
        self.btn_search = QtWidgets.QPushButton(self)
        self.btn_search.setText('pesquisar')
        self.gridLayout.addWidget(self.btn_search, 0, 1, 1, 1)
        self.tableWidget = Table(self)
        self.gridLayout.addWidget(self.tableWidget, 1, 0, 1, 2)
        self.show()

        self.btn_search.clicked.connect(lambda:self.tableWidget.search(self.ln_processos.text()))

