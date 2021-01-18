import datetime
import math

import psutil
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from src.processOptions import ProcessOptions
from src.tabs.dedicatedProcessWindow import DedicatedProcessWindow

memory = psutil.virtual_memory()[0]
memory = memory // (1024 * 1024)  # MB
cpu_count = psutil.cpu_count()


class Item(QtWidgets.QTableWidgetItem):
    def __init__(self, name):
        super(Item, self).__init__(name)
        self.setFlags(QtCore.Qt.ItemIsEnabled)

    def __lt__(self, other):
        if (isinstance(other, QtWidgets.QTableWidgetItem)):
            if self.data(QtCore.Qt.EditRole).isnumeric():
                my_value = float(self.data(QtCore.Qt.EditRole))
                if other.data(QtCore.Qt.EditRole).isnumeric():
                    other_value = float(other.data(QtCore.Qt.EditRole))
                    return my_value < other_value

        return super(Item, self).__lt__(other)


class Table(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super(Table, self).__init__(parent=parent)
        self.headings = ['name', 'cpu_percent', 'memory_percent', 'create_time', 'status', 'username', 'pid']
        self.searchTxt = None
        self.processOptions = None
        self.setMouseTracking(True)
        self.setColumnCount(len(self.headings))
        self.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.setSortingEnabled(True)
        for column, item in enumerate(self.headings):
            self.setHorizontalHeaderItem(column, QtWidgets.QTableWidgetItem(item))

        self.lastProcesses = {}
        row = 0
        for proc in psutil.process_iter(self.headings):
            proc.row = row
            row += 1
            self.lastProcesses[proc.pid] = proc

        self.setRowCount(row)
        for proc in self.lastProcesses:
            row = self.lastProcesses[proc].row
            self.setItem(row, 0, Item(self.lastProcesses[proc].name()))
            self.setItem(row, 1, Item((self.lastProcesses[proc].cpu_percent() / cpu_count).__str__()))

            self.setItem(row, 2,
                         Item((math.trunc(self.lastProcesses[proc].memory_percent() * memory // 100)).__str__()))
            creation_time = datetime.datetime.fromtimestamp(self.lastProcesses[proc].create_time()).strftime(
                "%Y-%m-%d %H:%M:%S")
            creation_time = creation_time.split(' ')[-1]
            self.setItem(row, 3, Item(creation_time))
            self.setItem(row, 4, Item(self.lastProcesses[proc].status()))
            self.setItem(row, 5, Item(self.lastProcesses[proc].username()))
            self.setItem(row, 6, Item(self.lastProcesses[proc].pid.__str__()))

        self._update()
        self.timer = QtCore.QTimer(interval=2000, timeout=self._update)
        self.timer.start()

    def _update(self):
        current = {}
        row = 0
        for proc in psutil.process_iter(self.headings):
            proc.row = row
            current[proc.pid] = proc
            row += 1

        rowCount = 0
        try:
            for proc in self.lastProcesses:
                row = self.lastProcesses[proc].row
                if proc in current:
                    self.setItem(row, 1, Item((self.lastProcesses[proc].cpu_percent() / cpu_count).__str__()))
                    self.setItem(row, 2, Item(
                        (math.trunc(self.lastProcesses[proc].memory_percent() * memory // 100)).__str__()))
                    self.setItem(row, 4, Item(self.lastProcesses[proc].status()))
                    rowCount += 1
                else:
                    self.removeRow(row)
        except psutil.NoSuchProcess:
            self.removeRow(row)

        newProcess = [proc for proc in current if proc not in self.lastProcesses]
        rows = len(current)
        self.setRowCount(rows)
        for index, proc in enumerate(newProcess):
            self.setItem(rowCount, 0, Item(current[proc].name()))
            self.setItem(rowCount, 1, Item((current[proc].cpu_percent() / cpu_count).__str__()))
            self.setItem(rowCount, 2, Item((math.trunc(current[proc].memory_percent() * memory // 100)).__str__()))
            creation_time = datetime.datetime.fromtimestamp(current[proc].create_time()).strftime("%Y-%m-%d %H:%M:%S")
            creation_time = creation_time.split(' ')[-1]
            self.setItem(rowCount, 3, Item(creation_time))
            self.setItem(rowCount, 4, Item(current[proc].status()))
            self.setItem(rowCount, 5, Item(current[proc].username()))
            self.setItem(rowCount, 6, Item(current[proc].pid.__str__()))
            rowCount += 1

        self.lastProcesses = current
        if self.searchTxt:
            self.search(self.searchTxt)

    def search(self, txt):
        self.searchTxt = txt
        self.showRows()
        if not txt:
            self.searchTxt = None
            return
        for i in range(self.rowCount()):
            item = self.item(i, 0)
            if item and item.text().__contains__(txt):
                continue
            self.hideRow(i)

    def showRows(self):
        for row in range(self.rowCount()):
            self.showRow(row)

    def mousePressEvent(self, e: QtGui.QMouseEvent):
        if e.buttons() == QtCore.Qt.RightButton:
            row = self.rowAt(e.y())
            if row:
                pid = int(self.item(row, 6).text())
                self.processOptions = ProcessOptions(pid, position=e.pos(), parent=self)

    def mouseMoveEvent(self, e: QtGui.QMouseEvent):
        if self.processOptions:
            if not self.processOptions.rect().contains(e.pos()):
                self.processOptions.close()

    def mouseDoubleClickEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            try:
                row = self.rowAt(event.y())
                self.item(row, 6)
                pid = int(self.item(row, 6).text())
                self.dedicateWindow = DedicatedProcessWindow(pid)
            except Exception:
                pass
