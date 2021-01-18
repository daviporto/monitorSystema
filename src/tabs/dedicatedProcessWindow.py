import datetime
import sys

import psutil
from PyQt5 import QtCore
from PyQt5 import QtWidgets

from src.charts.tampleteSingleProcess import TampleteSingleProcess

cpu_count = psutil.cpu_count()
memory = psutil.virtual_memory()[0]
memory = memory // (1024 * 1024)  # MB


class DedicatedProcessWindow(QtWidgets.QWidget):
    def __init__(self, pid, parent=None):
        super(DedicatedProcessWindow, self).__init__(parent=parent)
        try:
            process = psutil.Process(pid)
        except psutil.NoSuchProcess:
            QtWidgets.QMessageBox.warning(self,
                                          f"pid = {pid}",
                                          'processo inexistente')
            return

        self.process = process
        with process.oneshot():
            self.name = process.name()
            self.setWindowTitle(self.name)
            self.cpu_percent = process.cpu_percent()
            self.creation_time = datetime.datetime.fromtimestamp(process.create_time()).strftime("%Y-%m-%d %H:%M:%S")
            self.processStatus = process.status()
            self.memoryPercentage = process.memory_percent()
            self.numThread = process.num_threads()
            self.userName = process.username()

            self.groupBox = QtWidgets.QGroupBox(parent=self)
            formLayout = QtWidgets.QFormLayout(self.groupBox)
            formLayout.addRow('nome ->', QtWidgets.QLabel(self.name))
            formLayout.addRow('Pid ->', QtWidgets.QLabel('pid'))
            formLayout.addRow('data de inicialização ->', QtWidgets.QLabel(self.creation_time))
            formLayout.addRow('status do processo ->', QtWidgets.QLabel(self.processStatus))
            formLayout.addRow('numero de threads ->', QtWidgets.QLabel(self.numThread.__str__()))
            formLayout.addRow('nome do usuario ->', QtWidgets.QLabel(self.userName))

        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.addWidget(self.groupBox, 2, 0, 1, 2)
        self.cpuUltilizationChart = TampleteSingleProcess(parent=self,
                                                          seriesName='utilização do CPU(%)',
                                                          firstValue=self.cpu_percent)
        self.gridLayout.addWidget(self.cpuUltilizationChart, 0, 0, 1, 1)

        self.memoryUltilizationChart = TampleteSingleProcess(parent=self,
                                                             seriesName='ultilization memória ram (MB)',
                                                             yRange=(self.memoryPercentage * memory / 100) + 100,
                                                             firstValue=self.memoryPercentage * memory / 100
                                                             )
        self.gridLayout.addWidget(self.memoryUltilizationChart, 0, 1, 1, 1)

        txt = "max = {}, min = {}".format(self.cpuUltilizationChart.max,
                                          self.cpuUltilizationChart.min)
        self.lblCpuUsagemMetrics = QtWidgets.QLabel(self, text=txt)
        self.lblCpuUsagemMetrics.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout.addWidget(self.lblCpuUsagemMetrics, 1, 0, 1, 1)

        txt = "max = {:.0f}, medio = {:.0f}, min = {:.0f}".format(self.memoryUltilizationChart.max,
                                                                  self.memoryUltilizationChart.average,
                                                                  self.memoryUltilizationChart.min)
        self.lblMemoryUsagemMetrics = QtWidgets.QLabel(self, text=txt)
        self.lblMemoryUsagemMetrics.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout.addWidget(self.lblMemoryUsagemMetrics, 1, 1, 1, 1, )

        self.resize(800, 500)
        self.show()
        self.timer = QtCore.QTimer(interval=100, timeout=self._update)
        self.timer.start()

    def _update(self):
        try:
            self.cpuUltilizationChart.refresh_stats(self.process.cpu_percent() / cpu_count)
            txt = "max = {}, min = {}".format(self.cpuUltilizationChart.max,
                                              self.cpuUltilizationChart.min)
            self.lblCpuUsagemMetrics.setText(txt)

            self.memoryUltilizationChart.refresh_stats(self.process.memory_percent() * memory // 100)
            txt = "max = {:.2f}, medio = {:.2f}, min = {:.2f}".format(self.memoryUltilizationChart.max,
                                                                      self.memoryUltilizationChart.average,
                                                                      self.memoryUltilizationChart.min)
            self.lblMemoryUsagemMetrics.setText(txt)
        except psutil.NoSuchProcess:
            QtWidgets.QMessageBox.Warning(self,
                                          self.name,
                                          f'O processo {self.name} foi finalizado')

            self.destroy()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mw = DedicatedProcessWindow(1)
    sys.exit(app.exec())
