import sys

import qdarkstyle
from PyQt5 import QtWidgets

from src.tabs.process import ProcessTab
from src.tabs.resources import ResousesTab


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        """MainWindow constructor"""
        super().__init__()
        # Main UI code goes here
        tabs = QtWidgets.QTabWidget(self)
        self.setCentralWidget(tabs)
        processTab = ProcessTab(self)
        tabs.addTab(processTab, "processos")
        resourcesTab = ResousesTab(self)
        tabs.addTab(resourcesTab, "recursos")
        self.resize(800,500)
        # End main UI code
        self.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    mw = MainWindow()
    sys.exit(app.exec())