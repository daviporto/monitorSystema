from PyQt5 import QtCore
from PyQt5 import QtWidgets


class Item(QtWidgets.QTableWidgetItem):
    def __init__(self, name):
        super(Item, self).__init__(name)
        self.setFlags(QtCore.Qt.ItemIsEnabled)


class DescriptionTable(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super(DescriptionTable, self).__init__(parent=parent)
        self.setColumnCount(2)
        self.rows = 0

    def apendItem(self, name, description):
        self.rows += 1
        self.setRowCount(self.rows)
        self.setItem(self.rows, 0, Item(name))
        self.setItem(self.rows, 1, Item(description))
