import sys

from PyQt5 import QtWidgets

from src.charts.cpuFrequency import CPUFrequencyView
from src.charts.cpuUsage import CPUUsageView
from src.charts.diskUsage import DiskUsageView
from src.charts.memory import MemoryUsageView
from src.charts.net import NetUsageView


class ResousesTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ResousesTab, self).__init__(parent=parent)
        gridLayout = QtWidgets.QGridLayout(self)
        frequencyChart = CPUFrequencyView(self)
        cpuUsageChart = CPUUsageView(self)
        memoryChart = MemoryUsageView(self)
        diskUsageChart = DiskUsageView(self)
        netChart = NetUsageView(self)

        gridLayout.addWidget(frequencyChart, 0, 0, 1, 1)
        gridLayout.addWidget(cpuUsageChart, 0, 1, 1, 1)
        gridLayout.addWidget(memoryChart, 1, 0, 1, 2)
        gridLayout.addWidget(diskUsageChart, 2, 0, 1, 1)
        gridLayout.addWidget(netChart, 2, 1, 1, 1)
        self.gridLayout = gridLayout
        self.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mv = ResousesTab()
    sys.exit(app.exec())
